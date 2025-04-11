import uuid
from pathlib import Path

from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from redis import asyncio as aioredis

from backend.db.main import get_session
from backend.log.logger import get_logger
from .service import FileManagerService
from backend.auth.dependencies import get_current_user
from .dependecies import get_redis
from .schemas import UploadFileResponse


logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

fm_router = APIRouter()
fm_service = FileManagerService()


@fm_router.post(
    "/upload_file",
    status_code=status.HTTP_201_CREATED,
    response_model=UploadFileResponse,
)
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    redis_client: aioredis.Redis = Depends(get_redis),
    current_user: dict = Depends(get_current_user),
):
    """Upload a file to User's Storage Provider(s)"""
    response = await fm_service.upload_file(session, redis_client, file, current_user.get("uid"))
    return response


@fm_router.get(
    "/list_files",
    status_code=status.HTTP_200_OK,
)
async def list_files(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
    redis_client: aioredis.Redis = Depends(get_redis),
):
    """List all files uploaded by User"""
    return await fm_service.list_files(session, redis_client,current_user.get("uid"))


@fm_router.delete("/delete_file")
async def delete_file(
    file_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Delete a file uploaded by User"""
    return await fm_service.delete_file(session, file_id, current_user.get("uid"))


@fm_router.get("/download_file")
async def download_file(
    file_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Download a file uploaded by User"""
    return await fm_service.download_file(session, file_id, current_user.get("uid"))


@fm_router.put("/rename_file")
async def rename_file(
    file_id: uuid.UUID,
    new_name: str,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Rename a file uploaded by User"""
    return await fm_service.rename_file(
        session, file_id, current_user.get("uid"), new_name
    )


@fm_router.get("/storage_usage")
async def get_storage_usage(
    session: AsyncSession = Depends(get_session),
    redis_client: aioredis.Redis = Depends(get_redis),
    current_user: dict = Depends(get_current_user),
):
    """Get Storage Usage of User"""
    usage = await fm_service.get_storage_usage(session, redis_client, current_user.get("uid"))
    return usage

@fm_router.get("/storage_providers")
async def get_storage_providers_info(
    session: AsyncSession = Depends(get_session),
    redis_client: aioredis.Redis = Depends(get_redis),
    current_user: dict = Depends(get_current_user),
):
    """Get Storage Providers of User"""
    providers = await fm_service.get_storage_providers_info(session, redis_client, current_user.get("uid"))
    return providers


@fm_router.get("/ping")
async def ping(cache: aioredis.Redis =Depends(get_redis)):
    """Ping the server"""
    # await cache.set("ping", "pong", ex=10)
    return {"message": "Pong"}
