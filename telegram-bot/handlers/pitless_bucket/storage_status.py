from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from handlers.pitless_bucket.constants import BACKEND_API_URL
from handlers.pitless_bucket.auth import get_firebase_id_token, get_user

storage_status_router = Router()


@storage_status_router.message(Command("status"))
async def cmd_storage_status(message: Message) -> None:
    """
    Command to check Pitless Bucket storage usage
    """
    telegram_id = int(message.from_user.id)
    data = await get_user(telegram_id)
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
            await message.answer(
                "Failed to retrieve storage status. Please try again later."
            )
            return

        storage_data = response.json()

    def convert_bytes(size_bytes):
        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        current_size = size_bytes
        while current_size >= 1024 and unit_index < len(units) - 1:
            current_size /= 1024
            unit_index += 1
        return f"{current_size:.2f} {units[unit_index]}"

    used = storage_data.get("used", 0)
    available = storage_data.get("available", 0)
    total = storage_data.get("total", 0)

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
