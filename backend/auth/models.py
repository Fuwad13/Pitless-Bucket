from datetime import datetime, timezone
from typing import List, Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSON, TIMESTAMP, BIGINT
from sqlmodel import Field, Relationship, SQLModel, Column


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
    display_name: str
    username: str
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    created_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))

    drives: List["GoogleDrive"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    files: List["FileInfo"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self):
        return f"<User(id={self.uid}, name={self.name}, email={self.email}, created_at={self.created_at})>"
