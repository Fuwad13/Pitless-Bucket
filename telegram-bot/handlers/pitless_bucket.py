from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import Config
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import httpx

pb_router = Router()

PB_SETTINGS = "http://localhost:3000/settings"
BACKEND_API_URL = "http://localhost:8000/api/v1"

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


@pb_router.message(Command("link"))
async def cmd_link_account(message: Message) -> None:
    """
    Command to link Pitless Bucket account to the bot
    """
    await message.answer(
        f"Please go to this link and link your telegram id to your Pitless Bucket account\n{PB_SETTINGS}\nYour telegram id is:"
    )
    await message.answer(f"{message.from_user.id}")


@pb_router.message(Command("files"))
async def cmd_list_files(message: Message) -> None:
    """
    Command to list all files in the Pitless Bucket
    """
    telegram_id = int(message.from_user.id)
    async with httpx.AsyncClient() as httpx_client:

        response = await httpx_client.get(
            f"{BACKEND_API_URL}/auth/get_firebase_uid_by_tgid?tg_id={telegram_id}"
        )
    data = response.json()
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        await message.answer("Please link your account first")
        return
    try:
        id_token = await get_firebase_id_token(firebase_uid)
    except Exception as e:
        await message.answer("Something went wrong. Please try again later")
        return
    headers = {"Authorization": f"Bearer {id_token}"}
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:

        response = await httpx_client.get(
            f"{BACKEND_API_URL}/file_manager/list_files", headers=headers
        )
        response = response.json()
    files_list = [file["file_name"] for file in response]
    files_list_str = "\n".join(files_list)
    # TODO: modify this to show files list in a better way
    await message.answer(f"Here are all your files:\n{files_list_str}")
