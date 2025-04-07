from aiogram.types import ReplyKeyboardRemove, KeyboardButton

button = KeyboardButton(text="/link")

kb = ReplyKeyboardRemove(
    keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True
)
