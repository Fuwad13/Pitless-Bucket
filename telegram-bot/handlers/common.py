from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from handlers.pitless_bucket.constants import HELP_TEXT
from views import get_help_view

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('Welcome to PitLess Bucket!')

@router.message(Command("help"))
async def cmd_help(message: Message):
    text, markup, photo_path = await get_help_view()
    photo = FSInputFile(photo_path, filename="help_pb.png")
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)