from pydantic import BaseModel, Field


class ChatInput(BaseModel):
    question: str
    session_id: str = Field(default=None)

class ChatResponse(BaseModel):
    answer: str
    session_id: str
