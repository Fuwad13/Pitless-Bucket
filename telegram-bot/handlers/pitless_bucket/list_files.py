from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from handlers.pitless_bucket.constants import BACKEND_API_URL, PB_SETTINGS
from handlers.pitless_bucket.auth import get_firebase_id_token, get_user

list_files_router = Router()

PB_SETTINGS = "http://localhost:3000/settings"
BACKEND_API_URL = "http://localhost:8000/api/v1"


@list_files_router.message(Command("files"))
async def cmd_list_files(message: Message) -> None:
    """
    Command to list all files in the Pitless Bucket
    """
    telegram_id = int(message.from_user.id)
    data = await get_user(telegram_id)
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

