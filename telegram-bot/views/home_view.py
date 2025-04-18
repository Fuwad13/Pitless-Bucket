from pathlib import Path
from typing import Dict, Tuple

from aiogram.types import InlineKeyboardMarkup

from .keyboards.inline import link_menu, start_menu


async def get_home_view(name: str, data: Dict) -> Tuple[str, InlineKeyboardMarkup, str]:
    """
        Returns the home view text, keyboard_markup and photo_path.

        Arguments:
            name: The name of the telegram user.
            data: The data of the Pitless Bucket user.
    """
    reply_text = f"Hello, <b>{name}!</b>\nWelcome to <b>Pitless Bucket Telegram Bot 🤖</b>.\n\n"
    firebase_uid = data.get("firebase_uid", None)
    if firebase_uid is not None:
        reply_text += (
            "Your have linked your Pitless Bucket account. ✅\n\n"
            f"username: {data.get('username')}\n"
            f"email: {data.get('email')}\n\n"
        )
        markup = start_menu
        photo_path = Path(__file__).parent.parent / "assets" / "home_pb.png"
        return reply_text, markup, photo_path
    else:
        reply_text += "To use this bot, please link your <b>Pitless Bucket</b> account using the /link command.\n\n"
        markup = link_menu
        photo_path = Path(__file__).parent.parent / "assets" / "account_not_found_pb.png"
        return reply_text, markup, photo_path
