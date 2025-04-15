import asyncio

import httpx
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from handlers.pitless_bucket.auth import get_firebase_id_token, get_user
from handlers.pitless_bucket.constants import BACKEND_API_URL, PB_SETTINGS
from views import (
    get_about_view,
    get_dashboard_view,
    get_file_list_view,
    get_help_view,
    get_home_view,
    get_settings_view,
    get_unlink_view,
)

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


@callback_router.callback_query(lambda cq: cq.data == "inline:storage_status")
async def handle_storage_status(callback_query: CallbackQuery):
    """
    Handle the callback query for the storage status button.
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
    await callback_query.answer("Fetching your storage status...")
    id_token = await get_firebase_id_token(firebase_uid)
    headers = {"Authorization": f"Bearer {id_token}"}
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:
        response = await httpx_client.get(
            f"{BACKEND_API_URL}/file_manager/storage_usage", headers=headers
        )
        storage_data = response.json()
    if response.status_code == 200:

        def convert_bytes(size_bytes):
            units = ["B", "KB", "MB", "GB", "TB"]
            unit_index = 0
            current_size = size_bytes
            while current_size >= 1024 and unit_index < len(units) - 1:
                current_size /= 1024
                unit_index += 1
            return f"{current_size:.2f} {units[unit_index]}"

        used = storage_data.get("used", 0)
        available = storage_data.get("available", 0)
        total = storage_data.get("total", 0)

        used_str = convert_bytes(used)
        available_str = convert_bytes(available)
        total_str = convert_bytes(total)

        text = (
            "Storage Status:\n"
            f"Used: {used_str}\n"
            f"Available: {available_str}\n"
            f"Total: {total_str}"
        )
        await callback_query.message.answer(text=text)
    else:
        text = "Something went wrong, please try again later.\n\n"
        await callback_query.message.answer(text=text)


# TODO: Change bot upload and download
@callback_router.callback_query(lambda cq: cq.data == "inline:upload")
async def handle_upload_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the upload button.
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
    await callback_query.answer("Here is how to upload a file...")
    text = (
        "To upload a file, please send the file to this chat.\n\n"
        "Then reply /upload to that message containing the file\n\n"
        "Please make sure the file size is within the allowed limit( 50MB as per Telegram Bot API limit)."
    )
    await callback_query.message.answer(text=text)


@callback_router.callback_query(lambda cq: cq.data == "inline:download")
async def handle_download_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the download button.
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
    await callback_query.answer("Here is how to download a file...")
    text = (
        "To download a file, use /download [filename] command\n\n"
        "Please make sure the file name is correct and exists in your Pitless Bucket account."
    )
    await callback_query.message.answer(text=text)


@callback_router.callback_query(lambda cq: cq.data == "inline:added_storage")
async def handle_added_storage_callback(callback_query: CallbackQuery):
    """
    Handle the callback query for the added storage button.
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
    await callback_query.answer("Getting storage provider info...")
    id_token = await get_firebase_id_token(firebase_uid)
    async with httpx.AsyncClient(timeout=10.0) as httpx_client:
        response = await httpx_client.get(
            f"{BACKEND_API_URL}/file_manager/storage_providers",
            headers={"Authorization": f"Bearer {id_token}"},
        )

    text = "Storage Providers:\n\n"
    if response.status_code == 200:
        storage_data = response.json()
        for provider in storage_data:
            text += f"Provider: {provider.get('provider_name')}\nEmail: {provider.get("email")}\n\n"
        if len(storage_data) == 0:
            text += "No storage providers found.\n\n"
    else:
        text = "Something went wrong, please try again later.\n\n"
    await callback_query.message.answer(text=text)
