import json
from pathlib import Path
import uuid

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
            stmt = (
                update(StorageProvider)
                .where(StorageProvider.uid == uuid.UUID(existing_drive.uid))
                .values(creds=creds.to_json())
            )
            await session.exec(stmt)
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
