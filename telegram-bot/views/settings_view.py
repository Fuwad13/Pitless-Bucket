from pathlib import Path
from typing import Tuple

from aiogram.types import InlineKeyboardMarkup

from .keyboards.inline import settings_menu


async def get_settings_view() -> Tuple[str, InlineKeyboardMarkup, str]:
    """"
        Returns the settings view text, keyboard_markup and photo_path.
    """
    text = "<b>Pitless Bucket</b> Settings:\n\n"
    markup = settings_menu
    photo_path = Path(__file__).parent.parent / "assets" / "settings_pb.png"
    return text, markup, photo_path