from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.db.main import get_session
from backend.config import Config
import json


auth_router = APIRouter()

SCOPES = [
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
    scopes=SCOPES,
    redirect_uri="http://localhost:8000/api/v1/auth/google/callback",
    autogenerate_code_verifier=True,
    code_verifier=None,
)


@auth_router.get("/google")
def auth_google() -> dict:
    """Returns the Google OAuth2 authorization URL"""
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true"
    )
    return {"auth_url": authorization_url}


@auth_router.get("/google/callback")
async def auth_callback(
    code: str, session: AsyncSession = Depends(get_session)
) -> dict:
    """Callback URL for Google OAuth2 authorization"""
    try:

        flow.fetch_token(code=code)
        creds = flow.credentials
        creds = Credentials.from_authorized_user_info(creds.to_json())
        service = build("oauth2", "v2", credentials=creds)
        user_info = service.userinfo().get().execute()

    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Something went wrong, please try again"
        )

    # Get user info from Google
    # Check if user exists
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        # Create new user
        user = User(name=user_info.get("name", "Unknown"), email=user_info["email"])
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create GoogleDrive entry
    existing_drive = (
        db.query(GoogleDrive).filter(GoogleDrive.email == user_info["email"]).first()
    )
    if existing_drive:
        stmt = (
            update(GoogleDrive)
            .where(GoogleDrive.email == user_info["email"])
            .values(creds=creds.to_json())
        )
        db.execute(stmt)
        db.commit()
        db.refresh(existing_drive)
    else:
        drive = GoogleDrive(
            user_id=user.id,
            email=user_info["email"],
            creds=creds.to_json(),
            total_space=15 * 1024**3,  # 15GB in bytes
        )
        db.add(drive)
        db.commit()
        db.refresh(drive)

    return {"message": "Authentication successful!"}
