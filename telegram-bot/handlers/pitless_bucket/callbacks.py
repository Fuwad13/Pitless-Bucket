import asyncio
from aiogram import Router
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from views import (
    get_dashboard_view,
    get_home_view,
    get_help_view,
    get_about_view,
    get_file_list_view,
    get_settings_view,
    get_unlink_view,
)
import httpx
from handlers.pitless_bucket.auth import get_user, get_firebase_id_token
from handlers.pitless_bucket.constants import PB_SETTINGS, BACKEND_API_URL

callback_router = Router()


@callback_router.callback_query(lambda cq: cq.data == "inline:dashboard")
async def handle_dashboard_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the dashboard button.
    """
    telegram_id = int(callback_query.from_user.id)
    data = await get_user(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        reply_text = f"Hello, <b>{callback_query.from_user.full_name}!</b>\nWelcome to <b>Pitless Bucket Telegram Bot 🤖</b>.\n\n"
        reply_text += "To use this bot, please link your <b>Pitless Bucket</b> account using the /link command.\n\n"
        await callback_query.answer("Please link your account first")
        await callback_query.message.answer(text=reply_text)
        await callback_query.message.delete()
        return

    await callback_query.answer("Naviagating to Dashboard...")
    text, markup, photo_path = await get_dashboard_view()
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)


@callback_router.callback_query(lambda cq: cq.data == "inline:home")
async def handle_home_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the home button.
    """

    telegram_id = int(callback_query.from_user.id)
    data = await get_user(telegram_id)
    name = (
        callback_query.from_user.full_name
        if callback_query.from_user.full_name
        else "User"
    )
    text, markup, photo_path = await get_home_view(name=name, data=data)
    await callback_query.answer("Navigating to Home...")
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)


@callback_router.callback_query(lambda cq: cq.data == "inline:link")
async def handle_link_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the link button.
    """
    await callback_query.answer("Please follow the instructions to link your account.")
    await callback_query.message.answer(
        text=f"Please go to this link and link your telegram id to your Pitless Bucket account\n{PB_SETTINGS}\nYour telegram id is:"
    )
    await callback_query.message.answer(f"{callback_query.from_user.id}")
    await asyncio.sleep(2)
    await callback_query.message.delete()


@callback_router.callback_query(lambda cq: cq.data == "inline:help")
async def handle_help_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the help button.
    """
    await callback_query.answer("Naviagating to Help...")
    text, markup, photo_path = await get_help_view()
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)


@callback_router.callback_query(lambda cq: cq.data == "inline:about")
async def handle_about_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the about button.
    """
    await callback_query.answer("Naviagating to About...")
    text, markup, photo_path = await get_about_view()
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)


@callback_router.callback_query(lambda cq: cq.data == "inline:files")
async def handle_files_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the files button.
    """
    await callback_query.answer("File list is loading...")
    telegram_id = int(callback_query.from_user.id)
    data = await get_user(telegram_id)
    text, markup, photo_path = await get_file_list_view(data=data)
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)


@callback_router.callback_query(lambda cq: cq.data == "inline:settings")
async def handle_settings_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the settings button.
    """
    await callback_query.answer("Naviagating to Settings...")
    text, markup, photo_path = await get_settings_view()
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)


@callback_router.callback_query(lambda cq: cq.data == "inline:add_gdrive")
async def handle_add_gdrive_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the add gdrive button.
    """
    telegram_id = int(callback_query.from_user.id)
    data = await get_user(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        reply_text = f"Hello, <b>{callback_query.from_user.full_name}!</b>\nWelcome to <b>Pitless Bucket Telegram Bot 🤖</b>.\n\n"
        reply_text += "To use this bot, please link your <b>Pitless Bucket</b> account using the /link command.\n\n"
        await callback_query.answer("Please link your account first")
        await callback_query.message.answer(text=reply_text)
        await callback_query.message.delete()
        return
    await callback_query.answer("Sending you the link to add gdrive...")
    id_token = await get_firebase_id_token(firebase_uid)
    headers = {"Authorization": f"Bearer {id_token}"}
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:
        response = await httpx_client.get(
            f"{BACKEND_API_URL}/auth/google", headers=headers
        )
        rsjson = response.json()
    if response.status_code == 200:
        text = (
            "Please follow the link to add your gdrive account to Pitless Bucket:\n\n"
            f'<a href="{rsjson['google_auth_url']}">Add Google Drive</a>\n\n'
        )
        await callback_query.message.answer(text=text)
    else:
        text = "Something went wrong, please try again later.\n\n"
        await callback_query.message.answer(text=text)


@callback_router.callback_query(lambda cq: cq.data == "inline:add_dropbox")
async def handle_add_dropbox_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the add dropbox button.
    """
    telegram_id = int(callback_query.from_user.id)
    data = await get_user(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        reply_text = f"Hello, <b>{callback_query.from_user.full_name}!</b>\nWelcome to <b>Pitless Bucket Telegram Bot 🤖</b>.\n\n"
        reply_text += "To use this bot, please link your <b>Pitless Bucket</b> account using the /link command.\n\n"
        await callback_query.answer("Please link your account first")
        await callback_query.message.answer(text=reply_text)
        await callback_query.message.delete()
        return
    await callback_query.answer("Sending you the link to add dropbox...")
    id_token = await get_firebase_id_token(firebase_uid)
    headers = {"Authorization": f"Bearer {id_token}"}
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:
        response = await httpx_client.get(
            f"{BACKEND_API_URL}/auth/dropbox", headers=headers
        )
        rsjson = response.json()
    if response.status_code == 200:
        text = (
            "Please follow the link to add your dropbox account to Pitless Bucket:\n\n"
            f'<a href="{rsjson['dropbox_auth_url']}">Add Dropbox</a>\n\n'
        )
        await callback_query.message.answer(text=text)
    else:
        text = "Something went wrong, please try again later.\n\n"
        await callback_query.message.answer(text=text)


@callback_router.callback_query(lambda cq: cq.data == "inline:unlink_tg")
async def handle_unlink_tg_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the unlink telegram button.
    """
    telegram_id = int(callback_query.from_user.id)
    data = await get_user(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        await callback_query.answer(
            "You don't have any account linked to your telegram id."
        )
        await callback_query.message.delete()
        return
    await callback_query.answer("Are you sure you want to unlink?...")
    text, markup, photo_path = await get_unlink_view()
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)


@callback_router.callback_query(lambda cq: cq.data == "inline:confirm_unlink")
async def handle_confirm_unlink(callback_query: CallbackQuery):
    """
    Handle the callback query for the confirm unlink button.
    """
    telegram_id = int(callback_query.from_user.id)
    data = await get_user(telegram_id)
    firebase_uid = data.get("firebase_uid", None)
    if not firebase_uid:
        await callback_query.answer(
            "You don't have any account linked to your telegram id."
        )
        await callback_query.message.delete()
        return
    await callback_query.answer("Unlinking your telegram account...")
    id_token = await get_firebase_id_token(firebase_uid)
    headers = {"Authorization": f"Bearer {id_token}"}
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:
        response = await httpx_client.delete(
            f"{BACKEND_API_URL}/auth/unlink_telegram", headers=headers
        )
        if response.status_code == 200:
            await callback_query.message.answer(
                "✅ Your Telegram account has been successfully unlinked."
            )
            await callback_query.message.delete()
        else:
            await callback_query.message.answer(
                f"❌ Failed to unlink account: {response.text}"
            )


@callback_router.callback_query(lambda cq: cq.data == "inline:cancel_unlink")
async def handle_cancel_unlink(callback_query: CallbackQuery):
    """
    Handle the callback query for the cancel unlink button.
    """
    await callback_query.answer("Unlinking cancelled.")
    text, markup, photo_path = await get_settings_view()
    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=text)
    await callback_query.message.edit_media(media=media, reply_markup=markup)
