from datetime import datetime, timezone
from typing import List, Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSON, TIMESTAMP, BIGINT
from sqlmodel import Field, Relationship, SQLModel, Column, String

# --------------------------
# User Model
# --------------------------


class User(SQLModel, table=True):
    __tablename__ = "user"
    uid: uuid.UUID = Field(
        sa_column=Column(
            UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    firebase_uid: str = Field(index=True, sa_column_kwargs={"unique": True})
    display_name: str
    username: str
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    telegram_id: Optional[int] = Field(
        default=None, sa_column=Column(BIGINT, nullable=True)
    )
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))

    storage_providers: List["StorageProvider"] = Relationship(
        back_populates="firebase_user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    files: List["FileInfo"] = Relationship(
        back_populates="firebase_user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    def __repr__(self):
        return f"<User(id={self.uid}, display_name={self.display_name}, username={self.username}, email={self.email}, created_at={self.created_at})>"


# --------------------------
# StorageProvider Model
# --------------------------


class StorageProvider(SQLModel, table=True):
    __tablename__ = "storage_provider"

    uid: uuid.UUID = Field(
        sa_column=Column(
            UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    firebase_uid: str = Field(foreign_key="user.firebase_uid", index=True)
    provider_name: str = Field(sa_column=Column(String, nullable=False))
    email: str = Field(sa_column=Column(String, nullable=False))
    creds: dict = Field(sa_column=Column(JSON))
    used_space: int = Field(sa_column=Column(BIGINT), default=0)
    available_space: int = Field(sa_column=Column(BIGINT), default=0)

    firebase_user: "User" = Relationship(back_populates="storage_providers")
    chunks: List["FileChunk"] = Relationship(
        back_populates="provider",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    def __repr__(self):
        return (
            f"<StorageProvider(user_id={self.user_id}, provider_name={self.provider_name}, "
            f"used_space={self.used_space}, available_space={self.available_space})>"
        )


# --------------------------
# FileInfo Model
# --------------------------


class FileInfo(SQLModel, table=True):
    __tablename__ = "file_info"

    uid: uuid.UUID = Field(
        sa_column=Column(
            UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    firebase_uid: str = Field(foreign_key="user.firebase_uid", index=True)
    file_name: str
    content_type: str = Field(default="unknown_type")
    extension: str = Field(default="unknown_ext")
    size: int = Field(sa_column=Column(BIGINT))
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))

    firebase_user: "User" = Relationship(back_populates="files")
    chunks: List["FileChunk"] = Relationship(
        back_populates="file", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# --------------------------
# FileChunk Model
# --------------------------


class FileChunk(SQLModel, table=True):
    __tablename__ = "file_chunk"

    uid: uuid.UUID = Field(
        sa_column=Column(
            UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    file_id: uuid.UUID = Field(index=True, foreign_key="file_info.uid")
    chunk_name: str
    chunk_number: int
    provider_file_id: str
    provider_id: uuid.UUID = Field(foreign_key="storage_provider.uid")
    size: int = Field(sa_column=Column(BIGINT))
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))

    file: "FileInfo" = Relationship(back_populates="chunks")
    provider: "StorageProvider" = Relationship(back_populates="chunks")
