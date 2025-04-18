from pathlib import Path
from typing import Tuple

from aiogram.types import InlineKeyboardMarkup

from .keyboards.inline import help_menu


async def get_help_view() -> Tuple[str, InlineKeyboardMarkup, str]:
    """
        Returns the help view text and keyboard markup.
    """
    text = (
        "<b>Pitless Bucket Help</b>\n\n"
        "You can use the following commands:\n"
        "/start - Start using the bot\n"
        "/help - Show this help message\n"
        "/link - Link your Pitless Bucket account\n"
        "/unlink - Unlink your Pitless Bucket account\n"
        "/about - Show information about the bot\n"
        "/dashboard - Show your dashboard\n"
        "/settings - Show your settings\n"
        "/files - Show your files\n"
        "/status - Show your storage status\n"
        "/upload - Upload a file to your Pitless Bucket account\n"
        "/download - Download a file from your Pitless Bucket account\n"
    )
    markup = help_menu
    photo_path = Path(__file__).parent.parent / "assets" / "help_pb.png"
    return text, markup, photo_path