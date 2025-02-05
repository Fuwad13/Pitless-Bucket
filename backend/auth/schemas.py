from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class UserModel(BaseModel):
    uid: UUID = Field(default_factory=UUID)
    display_name: str
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<User(uid={self.uid}, display_name={self.display_name}, email={self.email}, created_at={self.created_at})>"
