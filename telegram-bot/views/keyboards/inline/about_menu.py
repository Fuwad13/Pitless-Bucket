from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


btn_settings = InlineKeyboardButton(text="Settings", callback_data="inline:settings")
btn_home = InlineKeyboardButton(text="Home", callback_data="inline:home")
btn_help = InlineKeyboardButton(text="Help", callback_data="inline:help")

kb_layout = [
    [btn_home, btn_settings, btn_help],
]

about_menu = InlineKeyboardMarkup(inline_keyboard=kb_layout)
