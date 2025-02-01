import os
import json
from pathlib import Path
import tempfile

from db.utils import get_db
from db.models import User, GoogleDrive, FileInfo, FileChunk
from fastapi import Depends
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from sqlalchemy.orm import Session
from sqlalchemy import update

app = FastAPI()

# CORS middleware to allow React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load client secrets from credentials.json
CLIENT_SECRETS_FILE = Path(__file__).parent / "credentials.json"
SCOPES = [
    "openid",  # Explicitly request OpenID Connect
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.metadata",
]

# Configure the OAuth2 flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="http://localhost:8000/auth/google/callback",
    autogenerate_code_verifier=True,
    code_verifier=None,
)


@app.get("/auth/google")
def auth_google():
    """Returns the Google OAuth2 authorization URL"""
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent", include_granted_scopes="true"
    )
    return {"auth_url": authorization_url}


@app.get("/auth/google/callback")
def auth_callback(code: str, db: Session = Depends(get_db)):
    """Callback URL for Google OAuth2 authorization"""
    flow.fetch_token(code=code)
    creds = flow.credentials
    with open(Path(__file__).parent / "temp_token.json", "w") as f:
        f.write(creds.to_json())
    creds = Credentials.from_authorized_user_file(
        Path(__file__).parent / "temp_token.json", SCOPES
    )
    # try:
    #     os.remove(Path(__file__).parent / 'temp_token.json')
    # except:
    #     pass

    # Get user info from Google
    service = build("oauth2", "v2", credentials=creds)
    user_info = service.userinfo().get().execute()
    # Check if user exists
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        # Create new user
        user = User(name=user_info.get("name", "Unknown"), email=user_info["email"])
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create GoogleDrive entry
    existing_drive = (
        db.query(GoogleDrive).filter(GoogleDrive.email == user_info["email"]).first()
    )
    if existing_drive:
        stmt = (
            update(GoogleDrive)
            .where(GoogleDrive.email == user_info["email"])
            .values(creds=creds.to_json())
        )
        db.execute(stmt)
        db.commit()
        db.refresh(existing_drive)
    else:
        drive = GoogleDrive(
            user_id=user.id,
            email=user_info["email"],
            creds=creds.to_json(),
            total_space=15 * 1024**3,  # 15GB in bytes
        )
        db.add(drive)
        db.commit()
        db.refresh(drive)

    return {"message": "Authentication successful!"}


@app.get("/api/files")
def list_files(db: Session = Depends(get_db)):
    # TODO : add JWT in headers
    # TODO : get creds from db
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("drive", "v3", credentials=creds)
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    return results.get("files", [])


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


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
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
            # Select account using round-robin
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
            user_id=1, file_name=file.filename, size=os.path.getsize(temp_file_path)
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
        if "temp_file_path" in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if "chunk_paths" in locals():
            for chunk_path in chunk_paths:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
