from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from config import Config
from handlers.pitless_bucket.auth import get_user

whoami_router = Router()


@whoami_router.message(Command("whoami"))
async def cmd_whoami(message: Message) -> None:
    try:
        telegram_id = message.from_user.id

        data = await get_user(telegram_id)

        firebase_uid = data.get("firebase_uid", None)
        if not firebase_uid:
            await message.answer(
                "❌ Your Pitless Bucket account is not linked. Please link your account first."
            )
            return
        user_name = data.get("username", "N/A")
        user_email = data.get("email", "N/A")
        await message.answer(
            f"✅ Connected Account:\nName: {user_name}\nEmail: {user_email}"
        )

    except httpx.ReadTimeout:
        await message.answer(
            "⚠️ Request timed out. Please check your connection and try again."
        )
    except httpx.ConnectError:
        await message.answer(
            "❌ Network error. Please try again later"
        )
    except Exception as e:
        await message.answer(f"NETWORK ERROR: {str(e)}")
        raise
