import asyncio
import logging
import sys, signal

from handlers.echo import echo_router
from handlers.start import start_router
from handlers.pitless_bucket.list_files import list_files_router
from handlers.pitless_bucket.storage_status import storage_status_router
from handlers.common import router as common_router
from handlers.pitless_bucket import (
    callback_router,
    upload_router,
    download_router,
    link_router,
    whoami_router,
    dashboard_router,
)

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
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
        link_router,
        whoami_router,
        callback_router,
        dashboard_router,
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    commands = [
        ("start", "Start using the bot"),
        ("help", "Get help"),
        ("dashboard", "Pitless Bucket dashboard"),
        ("upload", "Upload a file to your Pitless Bucket account"),
        ("link", "Link your Pitless Bucket account to the bot"),
        ("unlink", "Unlink (if linked) your Pitless Bucket account from the bot"),
        ("files", "List all files in your Pitless Bucket account"),
        ("whoami", "Get information about your Pitless Bucket account"),
    ]

    await bot.set_my_commands(
        commands=[
            BotCommand(command=command, description=description)
            for command, description in commands
        ]
    )

    await dp.start_polling(bot)


def signal_handler(signal, frame):
    print("Shutting down bot...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(asyncio.run(main()))
