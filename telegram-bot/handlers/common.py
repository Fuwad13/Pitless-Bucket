from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('Welcome to PitLess Bucket!')

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("""
        Available Commands:
        /start - Show welcome message
        /link - Link to your PitLess Bucket Account
        /files - List all available files
        /upload - Upload a new file
        /download [filename] Download a file by name
        /help - Show this help message
    """)