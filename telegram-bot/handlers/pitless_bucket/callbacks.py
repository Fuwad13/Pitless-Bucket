import asyncio
from aiogram import Router
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from views import get_dashboard_view, get_home_view
from handlers.pitless_bucket.auth import get_user
from handlers.pitless_bucket.constants import PB_SETTINGS, HELP_TEXT

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

    
