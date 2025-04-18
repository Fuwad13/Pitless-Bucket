from pathlib import Path
from typing import Tuple

from aiogram.types import InlineKeyboardMarkup

from .keyboards.inline import about_menu


async def get_about_view() -> Tuple[str, InlineKeyboardMarkup, str]:
    """
        Returns the help view text and keyboard markup.
    """
    text = (
        "<b>Pitless Bucket Bot</b>\n\n"
        "This bot is designed to help you manage your Pitless Bucket account.\n"
        "You can use it to link your account, upload and download files, and check your storage status.\n\n"
        "You can also use our Smart Assistant to get help about your files.\n"
    )
    markup = about_menu
    photo_path = Path(__file__).parent.parent / "assets" / "about_pb.png"
    return text, markup, photo_path