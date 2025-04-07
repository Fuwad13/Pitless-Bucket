from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_link = InlineKeyboardButton(text="Link Pitless Bucket Account", callback_data="inline:link")
btn_help = InlineKeyboardButton(text="Help", callback_data="inline:help")
btn_about = InlineKeyboardButton(text="About", callback_data="inline:about")

kb_layout = [
    [btn_link],
    [btn_help, btn_about],
]

link_menu = InlineKeyboardMarkup(inline_keyboard=kb_layout)
