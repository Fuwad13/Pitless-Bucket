from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class FileInfoResponseModel(BaseModel):
    uid: UUID
    firebase_id: UUID
    file_name: str
    content_type: str
    extension: str
    size: int
    created_at: datetime
    updated_at: datetime
