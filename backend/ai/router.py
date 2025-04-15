from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from redis import asyncio as aioredis
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.auth.dependencies import get_current_user
from backend.db.main import get_session
from backend.log.logger import get_logger

from .schemas import FileInfoResponse, StorageProviderInfo, UploadFileResponse

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

ai_router = APIRouter()

@ai_router.get("/invoke")
async def agent_invoke():
    return {"message": "Not yet implemented"}

