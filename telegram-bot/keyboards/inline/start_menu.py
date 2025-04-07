from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_dashboard = InlineKeyboardButton(text="Dashboard", callback_data="inline_dashboard")
btn_settings = InlineKeyboardButton(text="Settings", callback_data="inline_settings")
btn_help = InlineKeyboardButton(text="Help", callback_data="inline_help")
btn_about = InlineKeyboardButton(text="About", callback_data="inline_about")

kb_layout = [
    [btn_dashboard],
    [btn_settings],
    [btn_help, btn_about],
]

start_menu = InlineKeyboardMarkup(inline_keyboard=kb_layout)
