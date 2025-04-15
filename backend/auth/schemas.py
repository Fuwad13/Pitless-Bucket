from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    uid: UUID = Field(default_factory=UUID)
    firebase_uid: str
    display_name: str
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<User(uid={self.uid}, display_name={self.display_name}, email={self.email}, created_at={self.created_at})>"


class FirebaseUserModel(BaseModel):
    firebase_uid: str
    display_name: str
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<FirebaseUser(uid={self.uid}, display_name={self.display_name}, email={self.email}, created_at={self.created_at})>"
