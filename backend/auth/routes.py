from pathlib import Path
from fastapi import APIRouter, Depends
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


auth_router = APIRouter()

# Load client secrets from credentials.json
# TODO: handle this in more secure manner
CLIENT_SECRETS_FILE = Path(__file__).parent.parent / "credentials.json"
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.metadata",
]

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="http://localhost:8000/auth/google/callback",
    autogenerate_code_verifier=True,
    code_verifier=None,
)


@auth_router.get("/auth/google")
def auth_google() -> dict:
    """Returns the Google OAuth2 authorization URL"""
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true"
    )
    return {"auth_url": authorization_url}


# @auth_router.get("/auth/google/callback")
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
