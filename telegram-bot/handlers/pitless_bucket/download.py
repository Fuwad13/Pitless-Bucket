import os

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from handlers.pitless_bucket.auth import get_firebase_id_token, get_user
from handlers.pitless_bucket.constants import BACKEND_API_URL

download_router = Router()

# TODO: Refactor this to handle download more gracefully
@download_router.message(Command("download"))
async def cmd_download_file(message: Message) -> None:
    args = message.text.split()[1:]
    if not args:
        await message.answer("Usage: /download <filename>")
        return

    filename = " ".join(args).strip()

    try:
        telegram_id = message.from_user.id
        data_ = await get_user(telegram_id)
        firebase_uid = data_.get("firebase_uid", None)
        if not firebase_uid:
            await message.answer("Please link your account first using /link command.")
            return
        id_token = await get_firebase_id_token(firebase_uid)

        headers = {"Authorization": f"Bearer {id_token}"}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BACKEND_API_URL}/file_manager/list_files", headers=headers
            )
            if response.status_code != 200:
                await message.answer(f"Failed to fetch file list: {response.text}")
                return

            file_list = response.json()
            file_info = next((f for f in file_list if f["file_name"] == filename), None)
            if not file_info:
                await message.answer(
                    f"File '{filename}' not found in the available files."
                )
                return

            file_uid = file_info.get("uid")
            if not file_uid:
                await message.answer("File UID not found. Please contact support.")
                return

        async with httpx.AsyncClient(timeout=60.0) as client:
            await message.answer(f"Starting to download {filename}")
            response = await client.get(
                f"{BACKEND_API_URL}/file_manager/download_file",
                headers=headers,
                params={"file_id": file_uid},
            )
            if response.status_code != 200:
                await message.answer(f"Failed to download file: {response.text}")
                return

            content_disposition = response.headers.get("Content-Disposition", "")
            if "filename=" in content_disposition:
                downloaded_filename = content_disposition.split("filename=")[-1].strip(
                    '"'
                )
            else:
                downloaded_filename = file_info["file_name"]

            with open(downloaded_filename, "wb") as f:
                f.write(response.content)

            await message.answer_document(
                document=FSInputFile(downloaded_filename),
                caption=f"✅ File '{downloaded_filename}' downloaded successfully!",
            )
            os.remove(downloaded_filename)

    except httpx.ReadTimeout:
        await message.answer(
            "⚠️ Download timed out. Please check your connection and try again."
        )
    except httpx.ConnectError:
        await message.answer(
            "❌ Failed to connect to the server. Is the backend running?"
        )
    except Exception as e:
        await message.answer(f"NETWORK ERROR: {str(e)}")
        raise
