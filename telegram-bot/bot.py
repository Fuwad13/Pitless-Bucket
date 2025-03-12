import asyncio
import logging
from os import getenv

from handlers.echo import echo_router
from handlers.start import start_router
from handlers.pitless_bucket import pb_router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import Config

TOKEN = Config.TOKEN


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        # echo_router,
        pb_router,
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
