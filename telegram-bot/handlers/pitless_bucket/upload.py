from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, PhotoSize, Document, Video
import httpx
from handlers.pitless_bucket.constants import BACKEND_API_URL
from handlers.pitless_bucket.auth import get_firebase_id_token, get_user
import os

upload_router = Router()


@upload_router.message(Command("upload"))
async def cmd_upload_file(message: Message) -> None:

    file_to_upload = None

    if message.reply_to_message:
        replied_msg = message.reply_to_message
        if replied_msg.photo:
            await message.answer("Uploading image...")
            file_to_upload = replied_msg.photo[-1]
        elif replied_msg.document:
            file_to_upload = replied_msg.document
            await message.answer("Uploading document...")
        elif replied_msg.video:
            file_to_upload = replied_msg.video
            await message.answer("Uploading video...")
        else:
            await message.answer("The replied message doesn't contain a file.")
            return
    else:
        await message.answer("Reply to the file you want to upload with /upload")
        return

    try:
        if isinstance(file_to_upload, PhotoSize):
            file = await message.bot.download(file_to_upload)
            file_name = "image_tg.jpg"
            mime_type = "image/jpeg"
        elif isinstance(file_to_upload, Video):
            file = await message.bot.download(file_to_upload)
            original_name = file_to_upload.file_name
            _, ext = os.path.splitext(original_name) if original_name else ("", "")
            ext = ext.lower() or ".mp4"

            file_name = f"video_tg{ext}"
            mime_type = file_to_upload.mime_type or "video/mp4"

        elif isinstance(file_to_upload, Document):
            file = await message.bot.download(file_to_upload)

            original_name = file_to_upload.file_name
            _, ext = os.path.splitext(original_name) if original_name else ("", "")
            ext = ext.lower() or ".bin"

            file_name = f"file_tg{ext}"
            mime_type = file_to_upload.mime_type or "application/octet-stream"

        telegram_id = message.from_user.id
        data = await get_user(telegram_id)
        firebase_uid = data.get("firebase_uid")
        if not firebase_uid:
            await message.answer("Please link your account first using /link")
            return

        id_token = await get_firebase_id_token(firebase_uid)

        file_bytes = file.read()
        file.close()

        headers = {"Authorization": f"Bearer {id_token}"}
        files = {"file": (file_name, file_bytes, mime_type)}
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{BACKEND_API_URL}/file_manager/upload_file",
                headers=headers,
                files=files,
            )
            if response.status_code == 201 or response.status_code == 200:
                await message.answer("✅ File uploaded successfully!")
            else:
                await message.answer(
                    f"❌ Upload failed ({response.status_code}): {response.text}"
                )

    except httpx.ReadTimeout:
        await message.answer(
            "⚠️ Upload timed out. Please check your connection or try again later."
        )
    except httpx.ConnectError:
        await message.answer(
            "❌ Failed to connect to the server. Is the backend running?"
        )
    except Exception as e:
        await message.answer(f"NETWORK ERROR: {str(e)}")
        raise
