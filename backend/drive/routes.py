from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from backend.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import FileInfoModel, FileChunkModel, GoogleDriveModel

drive_router = APIRouter()


@drive_router.get("/files", response_model=List[FileInfoModel])
def list_files(session: AsyncSession = Depends(get_session)) -> List[FileInfoModel]:
    """List files from Google Drive ( currently sends only the filenames list )"""
    # TODO : add JWT in headers
    # TODO : get creds from db
    # this is now hardcoded for the demo
    # result = db.query(FileInfo).filter(FileInfo.user_id == 1).all()
    files = [
        {
            "name": file.file_name,
            "type": file.file_type,
            "id": file.id,
            "size": file.size,
        }
        for file in result
    ]
    return {"files": files}


def fetch_drive_service(email: str, db: Session):
    """Fetch Google Drive service for a specific user (Reuse credentials)"""
    drive_account = db.query(GoogleDrive).filter(GoogleDrive.email == email).first()
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


@drive_router.get("/api/get_file")
def get_file(file_id: int, db: Session = Depends(get_db)):
    """Reassemble and stream a file from its chunks with optimized performance"""
    file_info = db.query(FileInfo).filter(FileInfo.id == file_id).first()
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    file_chunks = (
        db.query(FileChunk)
        .filter(FileChunk.file_id == file_info.id)
        .order_by(FileChunk.chunk_number)
        .all()
    )
    if not file_chunks:
        raise HTTPException(status_code=404, detail="File chunks not found")

    # Prefetch all required drive services to avoid repeated database queries
    drive_accounts = {chunk.drive_account for chunk in file_chunks}
    drive_services = {
        account: fetch_drive_service(account, db) for account in drive_accounts
    }

    return StreamingResponse(
        chunk_generator(file_chunks, drive_services),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{file_info.file_name}"',
            "Content-Length": str(file_info.size),
            "Accept-Ranges": "bytes",
        },
    )


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


@drive_router.post("/api/upload")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = file.file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Split into 100MB chunks
        chunk_paths = split_file(temp_file_path)
        uploaded_chunks = []

        #  TODO : get creds from db , this is now hardcoded for the demo
        accounts_dir = Path(__file__).parent
        with open(accounts_dir / "RT_1.json") as f1, open(
            accounts_dir / "RT_2.json"
        ) as f2:
            accounts = [json.load(f1), json.load(f2)]

        current_account_idx = 0
        for idx, chunk_path in enumerate(chunk_paths):
            account = accounts[current_account_idx % len(accounts)]
            # Create credentials from account info
            creds = Credentials(
                token=None,
                refresh_token=account.get("refresh_token"),
                client_id=account.get("client_id"),
                client_secret=account.get("client_secret"),
                token_uri="https://oauth2.googleapis.com/token",
                scopes=SCOPES,
            )

            # TODO : handle this in a better way
            # Refresh token if needed
            # if not creds.valid:
            #     creds.refresh(Request())

            # Create Drive service
            drive_service = build("drive", "v3", credentials=creds)
            oauth_service = build("oauth2", "v2", credentials=creds)

            # Upload chunk
            chunk_name = f"{file.filename}.part{idx+1:03d}"
            file_metadata = {"name": chunk_name}
            media = MediaFileUpload(chunk_path, mimetype="application/octet-stream")

            drive_file = (
                drive_service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            # Store metadata
            uploaded_chunks.append(
                {
                    "original_filename": file.filename,
                    "chunk_number": idx + 1,
                    "chunk_name": chunk_name,
                    "drive_account": oauth_service.userinfo()
                    .get()
                    .execute()
                    .get("email"),
                    "drive_file_id": drive_file["id"],
                    "size": os.path.getsize(chunk_path),
                }
            )
            media._fd.close()
            print(chunk_path)
            current_account_idx += 1

        # TODO : currently hardcoded user_id
        file_ = FileInfo(
            user_id=1,
            file_name=file.filename,
            size=os.path.getsize(temp_file_path),
            file_type=file.content_type,
        )
        db.add(file_)
        db.commit()
        db.refresh(file_)
        for chunk in uploaded_chunks:
            db.add(
                FileChunk(
                    file_id=file_.id,
                    chunk_name=chunk["chunk_name"],
                    chunk_number=chunk["chunk_number"],
                    drive_file_id=chunk["drive_file_id"],
                    drive_account=chunk["drive_account"],
                    size=chunk["size"],
                )
            )
            db.commit()

        os.remove(temp_file_path)
        for chunk_path in chunk_paths:
            os.remove(chunk_path)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "total_chunks": len(chunk_paths),
            "chunks": uploaded_chunks,
        }

    except Exception as e:
        # Cleanup any remaining temporary files
        print(e)
        if "temp_file_path" in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if "chunk_paths" in locals():
            for chunk_path in chunk_paths:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@drive_router.delete("/api/delete_file")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """Delete a file from Google Drive"""
    #  TODO : check auth
    file_info = db.query(FileInfo).filter(FileInfo.id == file_id).first()
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    file_chunks = db.query(FileChunk).filter(FileChunk.file_id == file_id).all()
    if not file_chunks:
        db.delete(file_info)
        db.commit()
        raise HTTPException(status_code=404, detail="File chunks not found")

    for chunk in file_chunks:
        drive_mail = chunk.drive_account
        creds = (
            db.query(GoogleDrive).filter(GoogleDrive.email == drive_mail).first().creds
        )
        creds = Credentials.from_authorized_user_info(json.loads(creds))
        drive_service = build("drive", "v3", credentials=creds)
        drive_service.files().delete(fileId=chunk.drive_file_id).execute()
        db.delete(chunk)

    db.delete(file_info)
    db.commit()

    return {"message": "File deleted successfully"}


@drive_router.get("/api/drive_about")
def drive_about(db: Session = Depends(get_db), request: Request = None):
    """Get Google Drive about information for testing purposes."""
    # TODO: get creds from db, this is now hardcoded for the demo
    logger.debug("Getting drive about information")
    logger.info(f"Request from : {request.client.host}")
    accounts_dir = Path(__file__).parent
    with open(accounts_dir / "RT_1.json") as f:
        account = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=account.get("refresh_token"),
        client_id=account.get("client_id"),
        client_secret=account.get("client_secret"),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )

    drive_service = build("drive", "v3", credentials=creds)
    about_info = drive_service.about().get(fields="user, storageQuota").execute()
    filelist = drive_service.files().list(fields="*").execute()

    return {"about_info": filelist}
