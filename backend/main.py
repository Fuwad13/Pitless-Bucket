import io
from contextlib import asynccontextmanager
import os
import json
from pathlib import Path
import tempfile
from typing import List
import aiofiles
from backend.db.utils import get_db
from backend.db.models import User, GoogleDrive, FileInfo, FileChunk
from fastapi import Depends
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from sqlalchemy.orm import Session
from sqlalchemy import update
from backend.logs.logger import get_logger

logger = get_logger(__name__, Path(__file__).parent / "logs/app.log")


@asynccontextmanager
def life_span(app: FastAPI):
    logger.info("Server is starting......")
    yield
    logger.info("Server is shutting down......")


version = "v1"

app = FastAPI(
    title="Pitless Bucket",
    description="A REST API for Pitless Bucket - Distributed File Storage",
    version=version,
    lifespan=life_span,
)

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="localhost", port=8000, reload=True)
