from aiogram import Router
from aiogram.types import CallbackQuery

callback_router = Router()


@callback_router.callback_query(lambda cq: cq.data == "inline:dashboard")
async def handle_dashboard_callback(callback_query: CallbackQuery):
    await callback_query.answer("Naviagating to Dashboard...")
    # await callback_query.message.edit_text()
