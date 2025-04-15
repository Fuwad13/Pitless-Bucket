from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from views import get_home_view

from .pitless_bucket.auth import get_user

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
        Handle the start command.
    """

    data = await get_user(message.from_user.id)
    name = message.from_user.full_name if message.from_user.full_name else "User"
    text, markup, photo_path = await get_home_view(name=name, data=data)
    photo = FSInputFile(photo_path, filename="home_pb.png")
    await message.answer_photo(photo=photo,caption=text, reply_markup=markup)
