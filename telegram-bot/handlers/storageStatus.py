from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import Config
import httpx

storage_status_router = Router()

BACKEND_API_URL = "http://localhost:8000/api/v1"

async def get_firebase_id_token(uid: str) -> str:
    """
    Generate a Firebase ID token for the given user ID
    """
    from firebase_admin import auth as firebase_auth

    custom_token = firebase_auth.create_custom_token(uid)

    if isinstance(custom_token, bytes):
        custom_token = custom_token.decode("utf-8")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={Config.FIREBASE_API_KEY}"
    payload = {"token": custom_token, "returnSecureToken": True}
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.post(url, json=payload)
    if response.status_code == 200:
        id_token = response.json()["idToken"]
        return id_token
    else:
        raise Exception("Token exchange failed: " + response.text)


@storage_status_router.message(Command("status"))
async def cmd_storage_status(message: Message) -> None:
    """
    Command to check Pitless Bucket storage usage
    """
    telegram_id = int(message.from_user.id)
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.get(
            f"{BACKEND_API_URL}/auth/get_firebase_uid_by_tgid?tg_id={telegram_id}"
        )
    data = response.json()
    firebase_uid = data.get("firebase_uid", None)
    
    if not firebase_uid:
        await message.answer("Please link your account first using /link")
        return
    
    try:
        id_token = await get_firebase_id_token(firebase_uid)
    except Exception as e:
        await message.answer("Authentication failed. Please try again later.")
        return
    
    headers = {"Authorization": f"Bearer {id_token}"}
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:
        response = await httpx_client.get(
            f"{BACKEND_API_URL}/file_manager/storage_usage", headers=headers
        )
        
        if response.status_code != 200:
            await message.answer("Failed to retrieve storage status. Please try again later.")
            return
        
        storage_data = response.json()
    
    def convert_bytes(size_bytes):
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        current_size = size_bytes
        while current_size >= 1024 and unit_index < len(units) - 1:
            current_size /= 1024
            unit_index += 1
        return f"{current_size:.2f} {units[unit_index]}"
    
    used = storage_data.get('used', 0)
    available = storage_data.get('available', 0)
    total = storage_data.get('total', 0)
    
    used_str = convert_bytes(used)
    available_str = convert_bytes(available)
    total_str = convert_bytes(total)
    
    message_text = (
        "Storage Status:\n"
        f"Used: {used_str}\n"
        f"Available: {available_str}\n"
        f"Total: {total_str}"
    )
    
    await message.answer(message_text)