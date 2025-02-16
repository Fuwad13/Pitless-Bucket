from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from backend.config import Config
from pathlib import Path
from backend.log.logger import get_logger

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

FIREBASE_CLIENT_CREDS = {
    "type": "service_account",
    "project_id": Config.FIREBASE_PROJECT_ID,
    "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
    "private_key": Config.FIREBASE_PRIVATE_KEY,
    "client_email": Config.FIREBASE_CLIENT_EMAIL,
    "client_id": Config.FIREBASE_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": Config.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": Config.FIREBASE_CLIENT_X509_CERT_URL,
    "universe_domain": "googleapis.com",
}

# Initialize Firebase Admin (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CLIENT_CREDS)
    firebase_admin.initialize_app(cred)


class FirebaseTokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials

        try:
            decoded_token = firebase_auth.verify_id_token(token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired Firebase token",
            )
        return decoded_token


async def get_current_user(token_data: dict = Depends(FirebaseTokenBearer())) -> dict:
    """
    Dependency that returns the decoded Firebase token.
    """
    return token_data
