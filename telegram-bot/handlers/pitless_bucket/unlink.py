from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from handlers.pitless_bucket.constants import BACKEND_API_URL
from handlers.pitless_bucket.auth import get_firebase_id_token, get_user

logout_router = Router()


@logout_router.message(Command("unlink"))
async def cmd_logout(message: Message) -> None:
    try:
        telegram_id = message.from_user.id

        data = await get_user(telegram_id)

        firebase_uid = data.get("firebase_uid", None)
        if not firebase_uid:
            await message.answer(
                "No linked account found for this telegram account. Please use /link to link your account."
            )
            return

        id_token = await get_firebase_id_token(firebase_uid)

        headers = {"Authorization": f"Bearer {id_token}"}

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.delete(
                f"{BACKEND_API_URL}/auth/unlink_telegram", headers=headers
            )
            if response.status_code == 200:
                await message.answer(
                    "✅ Your Telegram account has been successfully unlinked."
                )
            else:
                await message.answer(f"❌ Failed to unlink account: {response.text}")

    except httpx.ReadTimeout:
        await message.answer(
            "⚠️ Request timed out. Please check your connection and try again."
        )
    except httpx.ConnectError:
        await message.answer(
            "❌ Failed to connect to the server. Is the backend running?"
        )
    except Exception as e:
        await message.answer(f"NETWORK ERROR: {str(e)}")
        raise
