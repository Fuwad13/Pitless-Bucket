import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, status

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, update

from backend.log.logger import get_logger
from backend.db.main import get_session
from backend.config import Config
from backend.db.models import User, StorageProvider
from .dependencies import get_current_user

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

CLIENT_SECRETS_WEB = {
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
    CLIENT_SECRETS_WEB,
    scopes=GOOGLE_DRIVE_SCOPES,
    redirect_uri="http://localhost:8000/api/v1/auth/google/callback",
    autogenerate_code_verifier=True,
    code_verifier=None,
)


@auth_router.get("/google", status_code=status.HTTP_200_OK)
def auth_google() -> dict:
    """Returns the Google OAuth2 authorization URL"""
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true"
    )
    return {"auth_url": authorization_url}


@auth_router.get("/google/callback", status_code=status.HTTP_200_OK)
async def auth_google_callback(
    code: str, session: AsyncSession = Depends(get_session)
) -> dict:
    """Callback URL for Google OAuth2 authorization"""
    try:

        #  TODO : run this block asynchronuouly
        flow.fetch_token(code=code)
        creds = flow.credentials
        creds = Credentials.from_authorized_user_info(json.loads(creds.to_json()))
        service = build("oauth2", "v2", credentials=creds)
        user_info = service.userinfo().get().execute()
        # TODO : check if user exists , for demo 1 it is not necessary
        stmt = select(User).where(User.email == user_info["email"])
        resutl = await session.exec(stmt)
        user = resutl.first()
        if not user:
            # create new user [ for demo 1 only ]
            user = User(
                display_name=user_info.get("name", "Unknown"),
                username=user_info.get("name", "Unknown"),
                email=user_info["email"],
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        existing_drive = (
            await session.exec(
                select(GoogleDrive).where(GoogleDrive.email == user_info["email"])
            )
        ).first()
        if existing_drive:
            stmt = (
                update(GoogleDrive)
                .where(GoogleDrive.email == user_info["email"])
                .values(creds=creds.to_json())
            )
            await session.exec(stmt)
            await session.commit()
            await session.refresh(existing_drive)
        else:
            drive = GoogleDrive(
                user_id=user.uid,
                email=user_info["email"],
                creds=creds.to_json(),
            )
            session.add(drive)
            await session.commit()
            await session.refresh(drive)

        return {"message": "Authentication successful!"}

    except Exception as e:
        logger.error(f"Error in auth_callback: {e}")
        raise HTTPException(
            status_code=400, detail="Something went wrong, please try again"
        )
