from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from handlers.pitless_bucket import BACKEND_API_URL, get_firebase_id_token
from dotenv import load_dotenv
import os

load_dotenv()
whoami_router = Router()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
@whoami_router.message(Command("whoami"))
async def cmd_whoami(message: Message) -> None:
    try:
        telegram_id = message.from_user.id

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{BACKEND_API_URL}/auth/get_firebase_uid_by_tgid?tg_id={telegram_id}"
            )
            if response.status_code != 200 or "firebase_uid" not in response.json():
                await message.answer("Not connected to any account.")
                return

            firebase_uid = response.json().get("firebase_uid")

        id_token = await get_firebase_id_token(firebase_uid)
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                "https://identitytoolkit.googleapis.com/v1/accounts:lookup",
                params={"key": FIREBASE_API_KEY},
                json={"idToken": id_token}
            )

            if response.status_code == 200:
                user_data = response.json().get("users", [{}])[0]
                user_name = user_data.get("displayName") or "Unknown Name"
                user_email = user_data.get("email") or "No Email Available"
                await message.answer(
                    f"✅ Connected Account:\nName: {user_name}\nEmail: {user_email}"
                )
            else:
                await message.answer(f"❌ Failed to fetch account details: {response.text}")

    except httpx.ReadTimeout:
        await message.answer("⚠️ Request timed out. Please check your connection and try again.")
    except httpx.ConnectError:
        await message.answer("❌ Failed to connect to the server. Is the backend running?")
    except Exception as e:
        await message.answer(f"NETWORK ERROR: {str(e)}")
        raise