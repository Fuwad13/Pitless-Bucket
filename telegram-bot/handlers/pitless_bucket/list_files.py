from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import httpx
from handlers.pitless_bucket.constants import BACKEND_API_URL, PB_SETTINGS
from handlers.pitless_bucket.auth import get_firebase_id_token, get_firebase_uid

list_files_router = Router()

PB_SETTINGS = "http://localhost:3000/settings"
BACKEND_API_URL = "http://localhost:8000/api/v1"


@list_files_router.message(Command("link"))
async def cmd_link_account(message: Message) -> None:
    """
    Command to link Pitless Bucket account to the bot
    """
    await message.answer(
        f"Please go to this link and link your telegram id to your Pitless Bucket account\n{PB_SETTINGS}\nYour telegram id is:"
    )
    await message.answer(f"{message.from_user.id}")


@list_files_router.message(Command("files"))
async def cmd_list_files(message: Message) -> None:
    """
    Command to list all files in the Pitless Bucket
    """
    telegram_id = int(message.from_user.id)
    data = await get_firebase_uid(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        await message.answer("Please link your account first")
        return
    try:
        id_token = await get_firebase_id_token(firebase_uid)
    except Exception as e:
        await message.answer("Something went wrong. Please try again later")
        return
    headers = {"Authorization": f"Bearer {id_token}"}
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:

        response = await httpx_client.get(
            f"{BACKEND_API_URL}/file_manager/list_files", headers=headers
        )
        response = response.json()
    files_list = [file["file_name"] for file in response]
    files_list_str = "\n".join(files_list)
    # TODO: modify this to show files list in a better way
    await message.answer(f"Here are all your files:\n{files_list_str}")


btn_inline_mode = InlineKeyboardButton(text="Inline Mode", callback_data="inline_mode")
btn_business_mode = InlineKeyboardButton(
    text="Business Mode", callback_data="business_mode"
)
btn_allow_groups = InlineKeyboardButton(
    text="Allow Groups?", callback_data="allow_groups"
)
btn_group_privacy = InlineKeyboardButton(
    text="Group Privacy", callback_data="group_privacy"
)
btn_group_admin = InlineKeyboardButton(
    text="Group Admin Rights", callback_data="group_admin"
)
btn_channel_admin = InlineKeyboardButton(
    text="Channel Admin Rights", callback_data="channel_admin"
)
btn_payments = InlineKeyboardButton(text="Payments", callback_data="payments")
btn_domain = InlineKeyboardButton(text="Domain", callback_data="domain")
btn_menu_button = InlineKeyboardButton(text="Menu Button", callback_data="menu_button")
btn_mini_app = InlineKeyboardButton(text="Configure Mini App", callback_data="mini_app")
btn_paid_broadcast = InlineKeyboardButton(
    text="Paid Broadcast", callback_data="paid_broadcast"
)
btn_back = InlineKeyboardButton(text="« Back to Bot", callback_data="back_to_bot")

# Arrange buttons into rows
rows = [
    [btn_inline_mode, btn_business_mode],  # Row 1: Two buttons
    [btn_allow_groups, btn_group_privacy],  # Row 2: Two buttons
    [btn_group_admin, btn_channel_admin],  # Row 3: Two buttons
    [btn_payments, btn_domain],  # Row 4: Two buttons
    [btn_menu_button],  # Row 5: One button
    [btn_mini_app],  # Row 6: One button
    [btn_paid_broadcast],  # Row 7: One button
    [btn_back],  # Row 8: One button
]

# Create the inline keyboard markup
settings_menu = InlineKeyboardMarkup(inline_keyboard=rows)


@list_files_router.message(Command("test"))
async def cmd_test(message: Message) -> None:
    """
    Command to test the bot
    """
    await message.answer("Test successful", reply_markup=settings_menu)
