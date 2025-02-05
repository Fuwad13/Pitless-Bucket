from pathlib import Path
from fastapi import APIRouter, Depends
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from backend.config import Config
from aiogoogle import Aiogoogle
from aiogoogle.auth.utils import create_secret
import json


auth_router = APIRouter()

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.metadata",
]

CLIENT_CREDS = {
    "client_id": Config.WEB_CLIENT_ID,
    "client_secret": Config.WEB_CLIENT_SECRET,
    "scopes": SCOPES,
    "redirect_uri": "http://localhost:8000/auth/google/callback",
}

aiogoogle = Aiogoogle(client_creds=CLIENT_CREDS)


@auth_router.get("/google")
def auth_google():
    """Returns the Google OAuth2 authorization URL"""

    if aiogoogle.oauth2.is_ready(CLIENT_CREDS):
        uri = aiogoogle.oauth2.authorization_url(
            client_creds=CLIENT_CREDS,
            state=create_secret(),
            access_type="offline",
            include_granted_scopes=True,
        )
        return {"auth_url": uri}
    else:
        return {"error": "Something went wrong!"}


# @auth_router.get("/google/callback")
# def auth_callback(code: str, db: Session = Depends(get_db)) -> dict:
#     """Callback URL for Google OAuth2 authorization"""
#     # TODO : handle errors
#     flow.fetch_token(code=code)
#     creds = flow.credentials
#     with open(Path(__file__).parent / "temp_token.json", "w") as f:
#         f.write(creds.to_json())
#     creds = Credentials.from_authorized_user_file(
#         Path(__file__).parent / "temp_token.json", SCOPES
#     )
#     # try:
#     #     os.remove(Path(__file__).parent / 'temp_token.json')
#     # except:
#     #     pass

#     # Get user info from Google
#     service = build("oauth2", "v2", credentials=creds)
#     user_info = service.userinfo().get().execute()
#     # Check if user exists
#     user = db.query(User).filter(User.email == user_info["email"]).first()
#     if not user:
#         # Create new user
#         user = User(name=user_info.get("name", "Unknown"), email=user_info["email"])
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     # Create GoogleDrive entry
#     existing_drive = (
#         db.query(GoogleDrive).filter(GoogleDrive.email == user_info["email"]).first()
#     )
#     if existing_drive:
#         stmt = (
#             update(GoogleDrive)
#             .where(GoogleDrive.email == user_info["email"])
#             .values(creds=creds.to_json())
#         )
#         db.execute(stmt)
#         db.commit()
#         db.refresh(existing_drive)
#     else:
#         drive = GoogleDrive(
#             user_id=user.id,
#             email=user_info["email"],
#             creds=creds.to_json(),
#             total_space=15 * 1024**3,  # 15GB in bytes
#         )
#         db.add(drive)
#         db.commit()
#         db.refresh(drive)

#     return {"message": "Authentication successful!"}
