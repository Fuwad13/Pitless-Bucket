from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import requests

router = Router()

@router.message(Command("view"))
async def list_files(message: Message):
    response = requests.get(LIST_FILES_API)
    if response.status_code == 200:
        files = "\n".join([item['file_name'] for item in response.json()])
        await message.answer(f"Available files:\n{files}")
    else:
        await message.answer("❌ Failed to fetch files")

@router.message(Command("upload"))
async def upload_file(message: Message):
    await message.answer("Please send the file to upload")

@router.message(F.document)
async def handle_upload(message: Message):
    await message.answer("File received")