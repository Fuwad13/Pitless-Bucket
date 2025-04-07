from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from handlers.pitless_bucket.constants import HELP_TEXT

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('Welcome to PitLess Bucket!')

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT)