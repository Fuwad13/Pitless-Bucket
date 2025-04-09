from aiogram.types import InlineKeyboardButton

btn_add_gdrive = InlineKeyboardButton(
    text="Add Google Drive", callback_data="inline:add_gdrive"
)
btn_add_dropbox = InlineKeyboardButton(
    text="Add Dropbox", callback_data="inline:add_dropbox"
)
btn_added_storage = InlineKeyboardButton(
    text="See added storage", callback_data="inline:added_storage"
)
btn_storage_status = InlineKeyboardButton(
    text="Storage status", callback_data="inline:storage_status"
)
btn_unlink_tg = InlineKeyboardButton(
    text="Unlink telegram", callback_data="inline:unlink_tg"
)
btn_help = InlineKeyboardButton(text="Help", callback_data="inline:help")
btn_about = InlineKeyboardButton(text="About", callback_data="inline:about")
btn_dashboard = InlineKeyboardButton(text="Dashboard", callback_data="inline:dashboard")
btn_settings = InlineKeyboardButton(text="Settings", callback_data="inline:settings")
btn_link = InlineKeyboardButton(
    text="Link Pitless Bucket Account", callback_data="inline:link"
)
btn_home = InlineKeyboardButton(text="Home", callback_data="inline:home")
btn_files = InlineKeyboardButton(text="My Files", callback_data="inline:files")
btn_upload = InlineKeyboardButton(text="Upload a file", callback_data="inline:upload")
btn_download = InlineKeyboardButton(
    text="Download a file", callback_data="inline:download"
)
