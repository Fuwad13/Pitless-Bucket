from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from handlers.pitless_bucket.auth import get_user
from views import get_file_list_view

list_files_router = Router()

@list_files_router.message(Command("files"))
async def cmd_list_files(message: Message) -> None:
    """
        Command to list all files in the Pitless Bucket
    """
    telegram_id = int(message.from_user.id)
    data = await get_user(telegram_id)
    text, markup, photo_path = await get_file_list_view(data=data)
    photo = FSInputFile(photo_path)
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)
    

