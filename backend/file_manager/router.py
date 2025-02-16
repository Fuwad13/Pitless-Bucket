import uuid
from pathlib import Path

from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.main import get_session
from backend.log.logger import get_logger
from .service import FileManagerService
from backend.auth.dependencies import get_current_user
from .schemas import FileInfoResponseModel


logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

fm_router = APIRouter()
fm_service = FileManagerService()


@fm_router.post("/upload_file", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Upload a file to User's Storage Provider(s)"""
    logger.debug(f"Current User: {current_user}")
    return await fm_service.upload_file(session, file, current_user.get("uid"))


@fm_router.get(
    "/list_files",
    status_code=status.HTTP_200_OK,
)
async def list_files(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """List all files uploaded by User"""
    logger.debug(f"Current User: {current_user}")
    return await fm_service.list_files(session, current_user.get("uid"))
