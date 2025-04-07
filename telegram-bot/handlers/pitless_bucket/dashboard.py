from pathlib import Path
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import httpx
from handlers.pitless_bucket.constants import BACKEND_API_URL, PB_SETTINGS
from handlers.pitless_bucket.auth import get_user
from views import get_dashboard_view

dashboard_router = Router()


@dashboard_router.message(Command("dashboard"))
async def cmd_dashboard(message: Message):
    """
    Pitless Bucket dashboard command
    """
    telegram_id = int(message.from_user.id)
    data = await get_user(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        reply_text = f"Hello, <b>{message.from_user.full_name}!</b>\nWelcome to <b>Pitless Bucket Telegram Bot 🤖</b>.\n\n"
        reply_text += "To use this bot, please link your <b>Pitless Bucket</b> account using the /link command.\n\n"
        await message.answer(text=reply_text)
        return
    text, markup, photo_path = await get_dashboard_view()
    # TODO: use the photo file id instead of the local file path
    photo = FSInputFile(photo_path, filename="dashboard.png")
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)
