from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


btn_settings = InlineKeyboardButton(text="Settings", callback_data="inline:settings")
btn_home = InlineKeyboardButton(text="Home", callback_data="inline:home")
btn_about = InlineKeyboardButton(text="About", callback_data="inline:about")

kb_layout = [
    [btn_home, btn_settings, btn_about],
]

help_menu = InlineKeyboardMarkup(inline_keyboard=kb_layout)
