from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

pb_router = Router()

PB_SETTINGS = "http://localhost:3000/settings"


@pb_router.message(Command("link"))
async def cmd_link_account(message: Message) -> None:
    """
    Command to link Pitless Bucket account to the bot
    """
    await message.answer(
        f"Please go to this link and link your telegram id to your Pitless Bucket account\n{PB_SETTINGS}\nYour telegram id is:"
    )
    await message.answer(f"{message.from_user.id}")


@pb_router.message(Command("files"))
async def cmd_list_files(message: Message) -> None:
    """
    Command to list all files in the Pitless Bucket
    """
    await message.answer("Here are all your files:")
