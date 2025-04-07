from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from .pitless_bucket.auth import get_firebase_id_token

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    pass
