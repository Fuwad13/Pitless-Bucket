from pathlib import Path
from typing import Tuple
from aiogram.types import InlineKeyboardMarkup
from .keyboards.inline import unlink_menu


async def get_unlink_view() -> Tuple[str, InlineKeyboardMarkup, str]:
    """ "
    Returns the settings view text, keyboard_markup and photo_path.
    """
    text = (
        "<b>Pitless Bucket</b> Settings:\n\n"
        "Are you sure you want to unlink your Pitless Bucket account from this telegram account?\n\n"
        "If you want to link your account again, please use the /link command."
    )
    markup = unlink_menu
    photo_path = Path(__file__).parent.parent / "assets" / "pitless_bucket.png"
    return text, markup, photo_path
