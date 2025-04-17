from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UploadFileResponse(BaseModel):
    uid: UUID
    firebase_uid: str
    file_name: str
    content_type: str
    extension: str
    size: int
    created_at: datetime
    updated_at: datetime


class StorageProviderInfo(BaseModel):
    provider_name: str
    email: str
    used_space: int
    available_space: int


class FileInfoResponse(BaseModel):
    uid: UUID
    firebase_uid: str
    file_name: str
    content_type: str
    extension: str
    size: int
    created_at: datetime
    updated_at: datetime
