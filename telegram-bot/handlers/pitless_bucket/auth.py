from config import Config
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import httpx
from .constants import FIREBASE_CLIENT_CREDS

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CLIENT_CREDS)
    firebase_admin.initialize_app(cred)


async def get_firebase_id_token(uid: str) -> str:
    """
    Generate a Firebase ID token for the given user ID
    """
    custom_token = firebase_auth.create_custom_token(uid)

    if isinstance(custom_token, bytes):
        custom_token = custom_token.decode("utf-8")

    # Exchange the custom token for an ID token using Firebase REST API
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={Config.FIREBASE_API_KEY}"
    payload = {"token": custom_token, "returnSecureToken": True}
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.post(url, json=payload)
    if response.status_code == 200:
        id_token = response.json()["idToken"]
        return id_token
    else:
        raise Exception("Token exchange failed: " + response.text)