import uuid
from pathlib import Path

from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.main import get_session
from backend.log.logger import get_logger

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

fm_router = APIRouter()


test_user_id: uuid.UUID = uuid.UUID("56fafb63-eeab-449d-8ea9-67503797c035")


@fm_router.post("/upload_file", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
):
    """Upload a file to User's Storage Provider(s)"""
    #  TODO: Implement file upload to Storage Provider(s)
    #
    pass
