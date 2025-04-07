from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_files = InlineKeyboardButton(text="My Files", callback_data="inline:files")
btn_upload = InlineKeyboardButton(text="Upload a file", callback_data="inline:upload")
btn_download = InlineKeyboardButton(text="Download a file", callback_data="inline:download")
btn_home = InlineKeyboardButton(text="Home", callback_data="inline:home")
btn_settings = InlineKeyboardButton(text="Settings", callback_data="inline:settings")
btn_help = InlineKeyboardButton(text="Help", callback_data="inline:help")
btn_about = InlineKeyboardButton(text="About", callback_data="inline:about")

kb_layout = [
    [btn_files],
    [btn_upload],
    [btn_download],
    [btn_home],
    [btn_settings],
    [btn_help, btn_about],
]

dashboard_menu = InlineKeyboardMarkup(inline_keyboard=kb_layout)
