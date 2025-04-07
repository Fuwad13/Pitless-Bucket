from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from handlers.pitless_bucket.constants import BACKEND_API_URL, PB_SETTINGS
from handlers.pitless_bucket.auth import get_firebase_id_token, get_user
from views import get_dashboard_view

dashboard_router = Router()

@dashboard_router.message(Command("dashboard"))
async def cmd_dashboard(message: Message):
    """
        Pitless Bucket dashboard command
    """
    text, markup = await get_dashboard_view()
    await message.answer(text, reply_markup=markup)
