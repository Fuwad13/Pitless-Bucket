from pathlib import Path
from typing import List

from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from redis import asyncio as aioredis

from backend.db.main import get_session
from backend.log.logger import get_logger
from backend.auth.dependencies import get_current_user
from .schemas import UploadFileResponse, StorageProviderInfo, FileInfoResponse


logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

aget_router = APIRouter()

@aget_router.get("/invoke")
async def agent_invoke():
    return {"message": "Not yet implemented"}