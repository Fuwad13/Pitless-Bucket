import json
from pathlib import Path
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import httpx
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, update

from backend.log.logger import get_logger
from backend.db.main import get_session
from backend.config import Config
from backend.db.models import User, StorageProvider
from .dependencies import get_current_user
from fastapi.responses import HTMLResponse
from .schemas import UserModel

logger = get_logger(
    __name__,
    Path(__file__).parent.parent / "log" / "app.log",
)


auth_router = APIRouter()

GOOGLE_DRIVE_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.metadata",
]

GOOGLE_CLIENT_SECRETS_WEB = {
    "web": {
        "client_id": Config.WEB_CLIENT_ID,
        "project_id": "cse327-project-449320",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": Config.WEB_CLIENT_SECRET,
        "redirect_uris": ["http://localhost:8000/api/v1/auth/google/callback"],
    }
}

flow = Flow.from_client_config(
    GOOGLE_CLIENT_SECRETS_WEB,
    scopes=GOOGLE_DRIVE_SCOPES,
    redirect_uri="http://localhost:8000/api/v1/auth/google/callback",
    autogenerate_code_verifier=True,
    code_verifier=None,
)


@auth_router.post("/register_user", status_code=status.HTTP_201_CREATED)
async def register_user(req: dict, session: AsyncSession = Depends(get_session)):
    """Register a user in database"""
    stmt = select(User).where(User.firebase_uid == req.get("firebase_uid"))
    existing_user = (await session.exec(stmt)).first()
    if existing_user:
        return existing_user
    user = User(**req)
    session.add(user)
    await session.commit()
    return user


@auth_router.get("/google", status_code=status.HTTP_200_OK)
def auth_google(current_user: dict = Depends(get_current_user)) -> dict:
    """Returns the Google OAuth2 authorization URL"""
    state = json.dumps({"user_id": str(current_user.get("uid"))})
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
        state=state,
    )
    return {"google_auth_url": authorization_url}


@auth_router.get("/google/callback", status_code=status.HTTP_200_OK)
async def auth_google_callback(
    code: str, state: str, session: AsyncSession = Depends(get_session)
) -> dict:
    """Callback URL for Google OAuth2 authorization"""
    try:
        state_data = json.loads(state)
        user_id = state_data.get("user_id")
        logger.debug(f"User ID: {user_id}")
        #  TODO : run this block asynchronuouly
        flow.fetch_token(code=code)
        creds = flow.credentials
        creds = Credentials.from_authorized_user_info(json.loads(creds.to_json()))
        service = build("oauth2", "v2", credentials=creds)
        user_info = service.userinfo().get().execute()

        existing_drive = (
            await session.exec(
                select(StorageProvider)
                .where(StorageProvider.provider_name == "google_drive")
                .where(StorageProvider.firebase_uid == user_id)
                .where(StorageProvider.email == user_info["email"])
            )
        ).first()
        if existing_drive:
            existing_drive.creds = creds.to_json()
            await session.commit()
        else:
            drive = StorageProvider(
                firebase_uid=user_id,
                provider_name="google_drive",
                email=user_info["email"],
                creds=creds.to_json(),
            )
            session.add(drive)
            await session.commit()

        html_content = "<html><body><h1>Authentication successful, You may close this window now.</h1></body></html>"
        return HTMLResponse(content=html_content)

    except Exception as e:
        await session.rollback()
        logger.error(f"Error in auth_callback: {e}")
        raise HTTPException(
            status_code=400, detail="Something went wrong, please try again"
        )


@auth_router.get("/dropbox")
def auth_dropbox(current_user: dict = Depends(get_current_user)) -> dict:
    """Returns the Dropbox OAuth2 authorization URL"""
    state = json.dumps({"user_id": str(current_user.get("uid"))})
    dropbox_auth_url = (
        f"https://www.dropbox.com/oauth2/authorize"
        f"?client_id={Config.DROPBOX_APP_KEY}"
        f"&response_type=code"
        f"&token_access_type=offline"
        f"&redirect_uri=http://localhost:8000/api/v1/auth/dropbox/callback"
        f"&state={state}"
    )
    return {"dropbox_auth_url": dropbox_auth_url}


@auth_router.get("/dropbox/callback", status_code=status.HTTP_200_OK)
async def auth_dropbox_callback(
    code: str, state: str, session: AsyncSession = Depends(get_session)
) -> dict:
    """Callback URL for Dropbox OAuth2 authorization"""
    try:
        state_data = json.loads(state)
        user_id = state_data.get("user_id")

        token_url = "https://api.dropboxapi.com/oauth2/token"
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": Config.DROPBOX_APP_KEY,
            "client_secret": Config.DROPBOX_APP_SECRET,
            "redirect_uri": "http://localhost:8000/api/v1/auth/dropbox/callback",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = httpx.post(token_url, data=data, headers=headers)
        token_data = response.json()

        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail="Failed to obtain access token")

        access_token = token_data["access_token"]
        refresh_token = token_data.get(
            "refresh_token"
        )  # Refresh token is returned only if offline access was requested
        expires_in = token_data["expires_in"]

        # Fetch Dropbox account details
        user_info_url = "https://api.dropboxapi.com/2/users/get_current_account"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = httpx.post(user_info_url, headers=headers)
        user_info = user_info_response.json()

        existing_drive = (
            await session.exec(
                select(StorageProvider)
                .where(StorageProvider.provider_name == "dropbox")
                .where(StorageProvider.firebase_uid == user_id)
                .where(StorageProvider.email == user_info["email"])
            )
        ).first()

        if existing_drive:
            existing_drive.creds = json.dumps(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": expires_in,
                }
            )
            await session.commit()
        else:
            dropbox_account = StorageProvider(
                firebase_uid=user_id,
                provider_name="dropbox",
                email=user_info["email"],
                creds=json.dumps(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "expires_in": expires_in,
                    }
                ),
            )
            session.add(dropbox_account)
            await session.commit()

        return HTMLResponse(
            content="<html><body><h1>Authentication successful, You may close this window now.</h1></body></html>"
        )

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error in Dropbox auth callback: {str(e)}"
        )
