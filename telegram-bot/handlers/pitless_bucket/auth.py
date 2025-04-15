from typing import Dict

import firebase_admin
import httpx
from config import Config
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

from .constants import BACKEND_API_URL, FIREBASE_CLIENT_CREDS

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


async def get_user(telegram_id: int) -> Dict:
    """
    Get the Firebase UID associated with the given Telegram ID
    """
    try:
        async with httpx.AsyncClient() as httpx_client:

            response = await httpx_client.get(
                f"{BACKEND_API_URL}/auth/get_user_by_tgid?tg_id={telegram_id}"
            )
        data = response.json()
        return data
    except Exception as e:
        print(f"Error getting firebase uid: {e}")
        return {"firebase_uid": None}


async def is_linked(telegram_id: int) -> bool:
    """
    Check if the telegram account is linked to a Pitless Bucket account
    """
    data = await get_user(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        return False
    return True
