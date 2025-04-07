from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from .pitless_bucket.auth import get_user
from keyboards.reply.link_cmd import kb as link_cmd_kb
from keyboards.inline import start_menu

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    reply_text = f"Hello, <b>{message.from_user.full_name}!</b>\nWelcome to <b>Pitless Bucket Telegram Bot 🤖</b>.\n\n"
    data = await get_user(message.from_user.id)
    firebase_uid = data.get("firebase_uid", None)
    if firebase_uid is not None:
        reply_text += (
            "Your Pitless Bucket account is already linked. ✅\n\n"
            f"username: {data.get('username')}\n"
            f"email: {data.get('email')}\n\n"
        )
        await message.answer(reply_text, reply_markup=start_menu)
    else:
        reply_text += (
            "To use this bot, please link your <b>Pitless Bucket</b> account using the /link command.\n\n"
            "You can also use the following commands:\n"
        )
        await message.answer(reply_text, reply_markup=link_cmd_kb)
