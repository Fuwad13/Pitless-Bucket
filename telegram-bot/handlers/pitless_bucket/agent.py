from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from handlers.pitless_bucket.auth import get_user, get_firebase_id_token
from handlers.pitless_bucket.constants import BACKEND_API_URL
import httpx

agent_router = Router()


@agent_router.message(F.text & ~F.text.startswith("/"))
async def text_handler(message: Message) -> None:
    """
    Handles text messages that are not commands.
    """
    user = await get_user(message.from_user.id)
    if user.get("firebase_uid", None):
        id_token = await get_firebase_id_token(user["firebase_uid"])
        headers = {
            "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
        }
        payload = {"question": message.text, "session_id": user["firebase_uid"]}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                BACKEND_API_URL + "/ai/chat", json=payload, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            await message.answer(data["answer"])

    else:
        await message.answer(
            "Please link your Pitless bucket account to use this bot. /link"
        )
