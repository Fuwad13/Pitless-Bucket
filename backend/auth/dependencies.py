from pathlib import Path

import firebase_admin
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

from backend.config import Config
from backend.log.logger import get_logger

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

FIREBASE_CLIENT_CREDS = {
    "type": "service_account",
    "project_id": Config.FIREBASE_PROJECT_ID,
    "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
    "private_key": Config.FIREBASE_PRIVATE_KEY_B64.replace("\\n", "\n"),
    "client_email": Config.FIREBASE_CLIENT_EMAIL,
    "client_id": Config.FIREBASE_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": Config.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": Config.FIREBASE_CLIENT_X509_CERT_URL,
    "universe_domain": "googleapis.com",
}

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
        # logger.debug(f"Decoded Firebase token: {decoded_token}")
        return decoded_token


async def get_current_user(token_data: dict = Depends(FirebaseTokenBearer())) -> dict:
    """
    Dependency that returns the decoded Firebase token.
    """
    return token_data
