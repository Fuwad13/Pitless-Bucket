from pathlib import Path
from typing import Tuple

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .keyboards.inline import dashboard_menu


async def get_dashboard_view() -> Tuple[str, InlineKeyboardMarkup, str]:
    """
        Returns the dashboard view text and keyboard markup.
    """
    text = f"<b>Pitless Bucket Dashboard</b>\n"
    markup = dashboard_menu
    photo_path = Path(__file__).parent.parent / "assets" / "dashboard_pb.png"
    return text, markup, photo_path
