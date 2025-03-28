import asyncio
import logging

from handlers.echo import echo_router
from handlers.start import start_router
from handlers.pitless_bucket.list_files import list_files_router
from handlers.pitless_bucket.storage_status import  storage_status_router
from handlers.common import router as common_router
from handlers.pitless_bucket.upload import upload_router
from handlers.pitless_bucket.download import download_router
from handlers.pitless_bucket.unlink import logout_router
from handlers.pitless_bucket.whoami import whoami_router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import Config

TOKEN = Config.TOKEN


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        storage_status_router,
        common_router,
        upload_router,
        download_router,
        list_files_router,
        logout_router,
        whoami_router,
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
