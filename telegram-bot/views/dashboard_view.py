from typing import Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .keyboards.inline import dashboard_menu

async def get_dashboard_view() -> Tuple[str, InlineKeyboardMarkup]:
    """
        Returns the dashboard view text and keyboard markup.
    """
    text = f"<b>Pitless Bucket Dashboard</b>\n"
    markup = dashboard_menu
    return text, markup
