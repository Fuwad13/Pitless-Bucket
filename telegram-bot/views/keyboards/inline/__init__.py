from aiogram.types import InlineKeyboardMarkup

from .buttons import (
    btn_about,
    btn_add_dropbox,
    btn_add_gdrive,
    btn_added_storage,
    btn_cancel_unlink,
    btn_confirm_unlink,
    btn_dashboard,
    btn_download,
    btn_files,
    btn_help,
    btn_home,
    btn_link,
    btn_settings,
    btn_storage_status,
    btn_unlink_tg,
    btn_upload,
)

about_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_home, btn_settings, btn_help],
    ]
)

dashboard_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_files],
        [btn_upload],
        [btn_download],
        [btn_home, btn_settings, btn_help, btn_about],
    ]
)

file_list_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_dashboard],
        [btn_home, btn_settings, btn_about],
    ]
)

help_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_home, btn_settings, btn_about],
    ]
)

link_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_link],
        [btn_help, btn_about],
    ]
)

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_dashboard],
        [btn_settings],
        [btn_help, btn_about],
    ]
)

settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_add_gdrive, btn_add_dropbox],
        [btn_added_storage, btn_storage_status],
        [btn_unlink_tg],
        [btn_home, btn_help, btn_about],
    ]
)

unlink_menu = InlineKeyboardMarkup(
    inline_keyboard=[[btn_confirm_unlink, btn_cancel_unlink]]
)
