from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)

test_router = Router()

b1 = KeyboardButton(text="1")
b2 = KeyboardButton(text="2")
keyboard = ReplyKeyboardRemove(
    keyboard=[[b1, b2]], resize_keyboard=True, one_time_keyboard=True
)


@test_router.message(Command("test1"))
async def cmd_test(message: Message):
    await message.reply("Testing", reply_markup=keyboard)
