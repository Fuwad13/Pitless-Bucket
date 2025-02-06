import asyncio
import json
import os
import io
import uuid
import tempfile
from typing import List
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import StreamingResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from backend.db.main import get_session
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.models import FileInfo, FileChunk, GoogleDrive, User
from .schemas import FileInfoModel, FileChunkModel, GoogleDriveModel
from backend.log.logger import get_logger
from .service import DriveService

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

drive_router = APIRouter()
drive_service = DriveService()

test_user_id: uuid.UUID = uuid.UUID("56fafb63-eeab-449d-8ea9-67503797c035")


@drive_router.get(
    "/files", response_model=List[FileInfoModel], status_code=status.HTTP_200_OK
)
async def list_files(
    session: AsyncSession = Depends(get_session),
) -> List[FileInfoModel]:
    """List files from Google Drive ( currently sends only the filenames list )"""
    # TODO : add JWT in headers
    # TODO : get creds from db
    # this is now hardcoded for the demo
    try:
        return await drive_service.get_files_by_user_id(session, str(test_user_id))
    except Exception as e:
        logger.error(f"Error in list_files: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


@drive_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
):
    """Upload a file to Google Drive in chunks and store metadata in the database"""
    try:
        async with aiofiles.tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # content = await file.read()
            while content := await file.read(1 * 1024 * 1024):
                await temp_file.write(content)
            temp_file_path = temp_file.name

        chunk_paths = await drive_service.async_split_file(temp_file_path)
        uploaded_chunks = []

        #  TODO : get creds from db , this is now hardcoded for the demo
        stmt = select(GoogleDrive)
        result = await session.exec(stmt)
        accounts = []
        for drive in result:
            oauth_service = await drive_service.async_get_api_service(
                "oauth2", "v2", drive.creds
            )
            mail_addr = oauth_service.userinfo().get().execute().get("email")
            gdrive_service = await drive_service.async_get_api_service(
                "drive", "v3", drive.creds
            )
            accounts.append(
                {
                    "account": mail_addr,
                    "creds": drive.creds,
                    "drive_service": gdrive_service,
                }
            )

        current_account_idx = 0
        for idx, chunk_path in enumerate(chunk_paths):
            account = accounts[current_account_idx % len(accounts)]
            # TODO : handle this in a better way
            # Refresh token if needed
            # if not creds.valid:
            #     creds.refresh(Request())

            # Upload chunk
            chunk_name = f"{file.filename}.part{idx+1:03d}"
            file_metadata = {"name": chunk_name}
            media = MediaFileUpload(chunk_path, mimetype="application/octet-stream")

            drive_file = await drive_service.async_upload_file(
                account["drive_service"], media, "id, size", body=file_metadata
            )
            uploaded_chunks.append(
                {
                    "original_filename": file.filename,
                    "chunk_number": idx + 1,
                    "chunk_name": chunk_name,
                    "drive_account": account["account"],
                    "drive_file_id": drive_file["id"],
                    "size": int(drive_file["size"]),
                }
            )
            media._fd.close()
            current_account_idx += 1

        # TODO : currently hardcoded user_id
        file_extension = (
            file.filename.split(".")[-1] if "." in file.filename else "unknown"
        )
        file_ = FileInfo(
            user_id=test_user_id,
            file_name=file.filename,
            content_type=file.content_type,
            extension=file_extension,
            size=file.size,
        )
        session.add(file_)
        await session.commit()
        await session.refresh(file_)
        for chunk in uploaded_chunks:
            chunk_to_add = FileChunk(
                file_id=file_.uid,
                chunk_name=chunk["chunk_name"],
                chunk_number=chunk["chunk_number"],
                drive_file_id=chunk["drive_file_id"],
                drive_account=chunk["drive_account"],
                size=chunk["size"],
            )
            session.add(chunk_to_add)
        await session.commit()

        await asyncio.to_thread(os.remove, temp_file_path)
        for chunk_path in chunk_paths:
            await asyncio.to_thread(os.remove, chunk_path)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "total_chunks": len(chunk_paths),
            "chunks": uploaded_chunks,
        }

    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        if "temp_file_path" in locals() and os.path.exists(temp_file_path):
            await aiofiles.os.remove(temp_file_path)
        if "chunk_paths" in locals():
            for chunk_path in chunk_paths:
                if await aiofiles.os.path.exists(chunk_path):
                    await aiofiles.os.remove(chunk_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@drive_router.delete("/delete_file", status_code=status.HTTP_200_OK)
async def delete_file(file_id: str, session: AsyncSession = Depends(get_session)):
    """Delete a file from Google Drive"""
    #  TODO : check auth
    stmt = select(FileInfo).where(FileInfo.uid == uuid.UUID(file_id))
    result = await session.exec(stmt)
    file_info = result.first()
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    stmt = select(FileChunk).where(FileChunk.file_id == file_info.uid)
    result = await session.exec(stmt)
    file_chunks = result.all()
    if not file_chunks:
        raise HTTPException(
            status_code=404, detail="File chunks for this file not found"
        )

    for chunk in file_chunks:
        drive_mail = chunk.drive_account
        creds = await drive_service.get_creds_by_gmail(session, drive_mail)
        gdrive_service = await drive_service.async_get_api_service("drive", "v3", creds)
        test = await drive_service.async_delete_file(
            gdrive_service, chunk.drive_file_id
        )
        await session.delete(chunk)
        logger.debug(f"{test}")
    logger.debug(f"Deleted {len(file_chunks)} chunks for file {file_info.file_name}")
    await session.delete(file_info)
    await session.commit()

    return {"message": "File deleted successfully"}


def fetch_drive_service(email: str, session: AsyncSession):
    """Fetch Google Drive service for a specific user (Reuse credentials)"""
    drive_account = (
        session.query(GoogleDrive).filter(GoogleDrive.email == email).first()
    )
    if not drive_account:
        raise HTTPException(status_code=500, detail=f"Drive account {email} not found")

    creds = Credentials.from_authorized_user_info(json.loads(drive_account.creds))
    return build("drive", "v3", credentials=creds)


def chunk_generator(file_chunks: List[FileChunk], drive_services):
    """Generator function to stream file chunks from Google Drive with optimized chunk size"""
    for idx, chunk in enumerate(file_chunks):
        drive_service = drive_services[chunk.drive_account]
        request = drive_service.files().get_media(fileId=chunk.drive_file_id)

        chunk_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(
            chunk_stream, request, chunksize=100 * 1024 * 1024
        )

        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.info(
                f"Downloading {chunk.chunk_name} chunk id : {chunk.chunk_number} - {status.progress() * 100:.2f}%"
            )
            chunk_stream.seek(0)
            data = chunk_stream.read()
            if data:
                yield data
            chunk_stream.seek(0)
            chunk_stream.truncate(0)


@drive_router.get("/download")
async def get_file(file_id: str, session: AsyncSession = Depends(get_session)):
    """Reassemble and stream a file from its chunks with optimized performance"""
    stmt = select(FileInfo).filter(FileInfo.uid == file_id)
    result = await session.exec(stmt)
    file_info = result.first()
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    stmt = select(FileChunk).where(FileChunk.file_id == file_info.uid)
    result = await session.exec(stmt)
    file_chunks = result.all()
    if not file_chunks:
        raise HTTPException(status_code=404, detail="File chunks not found")

    drive_accounts = {chunk.drive_account for chunk in file_chunks}
    gdrive_services = {
        acc: await drive_service.async_get_api_service_by_email(
            session, "drive", "v3", acc
        )
        for acc in drive_accounts
    }

    return StreamingResponse(
        chunk_generator(file_chunks, gdrive_services),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{file_info.file_name}"',
            "Content-Length": str(file_info.size),
            "Accept-Ranges": "bytes",
        },
    )


# @drive_router.get("/api/drive_about")
# def drive_about(db: Session = Depends(get_db), request: Request = None):
#     """Get Google Drive about information for testing purposes."""
#     # TODO: get creds from db, this is now hardcoded for the demo
#     logger.debug("Getting drive about information")
#     logger.info(f"Request from : {request.client.host}")
#     accounts_dir = Path(__file__).parent
#     with open(accounts_dir / "RT_1.json") as f:
#         account = json.load(f)

#     creds = Credentials(
#         token=None,
#         refresh_token=account.get("refresh_token"),
#         client_id=account.get("client_id"),
#         client_secret=account.get("client_secret"),
#         token_uri="https://oauth2.googleapis.com/token",
#         scopes=SCOPES,
#     )

#     drive_service = build("drive", "v3", credentials=creds)
#     about_info = drive_service.about().get(fields="user, storageQuota").execute()
#     filelist = drive_service.files().list(fields="*").execute()

#     return {"about_info": filelist}
