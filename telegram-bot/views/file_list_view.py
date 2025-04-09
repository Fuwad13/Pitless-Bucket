from pathlib import Path
from typing import Tuple, Dict
from aiogram.types import InlineKeyboardMarkup
import httpx
from .keyboards.inline import file_list_menu, link_menu
from handlers.pitless_bucket.auth import get_firebase_id_token
from handlers.pitless_bucket.constants import BACKEND_API_URL

# TODO: Polish this view
async def get_file_list_view(data: Dict) -> Tuple[str, InlineKeyboardMarkup, str]:
    """
        Returns the file list view text, keyboard_markup and photo_path.

        Arguments:
            data: The data of the Pitless Bucket user.
    """
    firebase_uid = data.get("firebase_uid", None)
    if firebase_uid is None:
        text = (
            "To use this bot, please link your <b>Pitless Bucket</b> account using the /link command.\n\n"
        )
        markup = link_menu
        photo_path = Path(__file__).parent.parent / "assets" / "account_not_found_pb.png"
        return text, markup, photo_path
    else:
        text = "Your files:\n\n"
        id_token = await get_firebase_id_token(firebase_uid)
        headers = {"Authorization": f"Bearer {id_token}"}
        async with httpx.AsyncClient(timeout=10.0) as httpx_client:

            response = await httpx_client.get(
                f"{BACKEND_API_URL}/file_manager/list_files", headers=headers
            )
            response = response.json()
        file_list = [(file["file_name"], file["size"], file["uid"]) for file in response]
        file_list_str = "\n".join(
            [file[0] for file in file_list]
        )
        if len(file_list_str) == 0:
            file_list_str = "No files found."
        text += file_list_str
        markup = file_list_menu
        photo_path = Path(__file__).parent.parent / "assets" / "my_files_pb.png"
        return text, markup, photo_path
    