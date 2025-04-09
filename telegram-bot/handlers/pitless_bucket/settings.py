from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from handlers.pitless_bucket.auth import get_user
from views import get_settings_view

settings_router = Router()

@settings_router.message(Command("settings"))
async def cmd_settings(message: Message) -> None:
    """
        Command to handle settings in the Pitless Bucket
    """
    text, markup, photo_path = await get_settings_view()
    photo = FSInputFile(photo_path)
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)