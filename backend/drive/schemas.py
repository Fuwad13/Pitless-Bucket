from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class GoogleDriveModel(BaseModel):
    uid: UUID
    user_id: UUID
    email: str
    creds: dict
    used_space: int
    available_space: int


class FileInfoModel(BaseModel):
    uid: UUID
    user_id: UUID
    file_name: str
    content_type: str
    extension: str
    size: int
    created_at: datetime
    updated_at: datetime


class FileChunkModel(BaseModel):
    uid: UUID
    file_id: UUID
    chunk_name: str
    chunk_number: int
    drive_file_id: str
    drive_account: str
    size: int
    created_at: datetime
    updated_at: datetime
