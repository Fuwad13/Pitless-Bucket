import json
import os
import uuid
import tempfile
from typing import List
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from backend.db.main import get_session
from googleapiclient.http import MediaFileUpload
from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.models import FileInfo, FileChunk, GoogleDrive, User
from .schemas import FileInfoModel, FileChunkModel, GoogleDriveModel
from backend.log.logger import get_logger

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

drive_router = APIRouter()

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
    # result = db.query(FileInfo).filter(FileInfo.user_id == 1).all()
    stmt = select(FileInfo).where(FileInfo.user_id == test_user_id)
    result = await session.exec(stmt)

    return result


@drive_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
):
    """Upload a file to Google Drive in chunks and store metadata in the database"""
    # try:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        content = file.file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    chunk_paths = split_file(temp_file_path)
    uploaded_chunks = []

    #  TODO : get creds from db , this is now hardcoded for the demo
    stmt = select(GoogleDrive)
    result = await session.exec(stmt)
    accounts = []
    for drive in result:
        creds = Credentials.from_authorized_user_info(json.loads(drive.creds))
        oauth_service = build("oauth2", "v2", credentials=creds)
        mail_addr = oauth_service.userinfo().get().execute().get("email")
        drive_service = build("drive", "v3", credentials=creds)
        accounts.append(
            {
                "account": mail_addr,
                "creds": drive.creds,
                "drive_service": drive_service,
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

        drive_file = (
            account["drive_service"]
            .files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        uploaded_chunks.append(
            {
                "original_filename": file.filename,
                "chunk_number": idx + 1,
                "chunk_name": chunk_name,
                "drive_account": account["account"],
                "drive_file_id": drive_file["id"],
                "size": os.path.getsize(chunk_path),
            }
        )
        media._fd.close()
        current_account_idx += 1

    # TODO : currently hardcoded user_id
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "unknown"
    file_ = FileInfo(
        user_id=test_user_id,
        file_name=file.filename,
        content_type=file.content_type,
        extension=file_extension,
        size=os.path.getsize(temp_file_path),
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

    os.remove(temp_file_path)
    for chunk_path in chunk_paths:
        os.remove(chunk_path)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "total_chunks": len(chunk_paths),
        "chunks": uploaded_chunks,
    }

    # except Exception as e:
    #     logger.error(f"Error in upload_file: {e}")
    #     if "temp_file_path" in locals() and os.path.exists(temp_file_path):
    #         os.remove(temp_file_path)
    #     if "chunk_paths" in locals():
    #         for chunk_path in chunk_paths:
    #             if os.path.exists(chunk_path):
    #                 os.remove(chunk_path)
    #     raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def split_file(input_file_path: str, chunk_size: int = 100 * 1024 * 1024) -> list[str]:
    """
    Split a file into chunks of specified size (default: 100MB).
    Returns a list of chunk file paths.
    """
    chunk_paths = []
    part_num = 1

    with open(input_file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            chunk_name = f"{input_file_path}.part{part_num}"
            with open(chunk_name, "wb") as chunk_file:
                chunk_file.write(chunk)

            chunk_paths.append(chunk_name)
            part_num += 1

    return chunk_paths


# def fetch_drive_service(email: str, db: Session):
#     """Fetch Google Drive service for a specific user (Reuse credentials)"""
#     drive_account = db.query(GoogleDrive).filter(GoogleDrive.email == email).first()
#     if not drive_account:
#         raise HTTPException(status_code=500, detail=f"Drive account {email} not found")

#     creds = Credentials.from_authorized_user_info(json.loads(drive_account.creds))
#     return build("drive", "v3", credentials=creds)


# def chunk_generator(file_chunks: List[FileChunk], drive_services):
#     """Generator function to stream file chunks from Google Drive with optimized chunk size"""
#     for idx, chunk in enumerate(file_chunks):
#         drive_service = drive_services[chunk.drive_account]
#         request = drive_service.files().get_media(fileId=chunk.drive_file_id)

#         chunk_stream = io.BytesIO()
#         downloader = MediaIoBaseDownload(
#             chunk_stream, request, chunksize=100 * 1024 * 1024
#         )

#         done = False
#         while not done:
#             status, done = downloader.next_chunk()
#             logger.info(
#                 f"Downloading {chunk.chunk_name} chunk id : {chunk.chunk_number} - {status.progress() * 100:.2f}%"
#             )
#             chunk_stream.seek(0)
#             data = chunk_stream.read()
#             if data:
#                 yield data
#             chunk_stream.seek(0)
#             chunk_stream.truncate(0)


# @drive_router.get("/api/get_file")
# def get_file(file_id: int, db: Session = Depends(get_db)):
#     """Reassemble and stream a file from its chunks with optimized performance"""
#     file_info = db.query(FileInfo).filter(FileInfo.id == file_id).first()
#     if not file_info:
#         raise HTTPException(status_code=404, detail="File not found")

#     file_chunks = (
#         db.query(FileChunk)
#         .filter(FileChunk.file_id == file_info.id)
#         .order_by(FileChunk.chunk_number)
#         .all()
#     )
#     if not file_chunks:
#         raise HTTPException(status_code=404, detail="File chunks not found")

#     # Prefetch all required drive services to avoid repeated database queries
#     drive_accounts = {chunk.drive_account for chunk in file_chunks}
#     drive_services = {
#         account: fetch_drive_service(account, db) for account in drive_accounts
#     }

#     return StreamingResponse(
#         chunk_generator(file_chunks, drive_services),
#         media_type="application/octet-stream",
#         headers={
#             "Content-Disposition": f'attachment; filename="{file_info.file_name}"',
#             "Content-Length": str(file_info.size),
#             "Accept-Ranges": "bytes",
#         },
#     )


# @drive_router.delete("/api/delete_file")
# def delete_file(file_id: int, db: Session = Depends(get_db)):
#     """Delete a file from Google Drive"""
#     #  TODO : check auth
#     file_info = db.query(FileInfo).filter(FileInfo.id == file_id).first()
#     if not file_info:
#         raise HTTPException(status_code=404, detail="File not found")

#     file_chunks = db.query(FileChunk).filter(FileChunk.file_id == file_id).all()
#     if not file_chunks:
#         db.delete(file_info)
#         db.commit()
#         raise HTTPException(status_code=404, detail="File chunks not found")

#     for chunk in file_chunks:
#         drive_mail = chunk.drive_account
#         creds = (
#             db.query(GoogleDrive).filter(GoogleDrive.email == drive_mail).first().creds
#         )
#         creds = Credentials.from_authorized_user_info(json.loads(creds))
#         drive_service = build("drive", "v3", credentials=creds)
#         drive_service.files().delete(fileId=chunk.drive_file_id).execute()
#         db.delete(chunk)

#     db.delete(file_info)
#     db.commit()

#     return {"message": "File deleted successfully"}


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
