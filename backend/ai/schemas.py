from pydantic import BaseModel, Field


class ChatInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
