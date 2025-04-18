from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from redis import asyncio as aioredis
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.auth.dependencies import get_current_user
from backend.db.main import get_session
from backend.log.logger import get_logger
from .agents import chatbot_agent, chatbot_agent2
from langchain_core.messages import HumanMessage
from .schemas import ChatInput, ChatResponse


logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

ai_router = APIRouter()

@ai_router.get("/invoke_test")
async def agent_invoke_test(q: str, session: AsyncSession = Depends(get_session)):
    ret = await chatbot_agent2.ainvoke(
        input={"user_id": "6OJvZ9a5FFWGvTHsuxTMWjVfkOj2","messages": [HumanMessage(content=q)]},
        config={"configurable": {"thread_id": "user_id_here"}},
    )
    return ret


@ai_router.post("/chat", response_model=ChatResponse)
async def agent_invoke(chat_input: ChatInput, current_user: dict = Depends(get_current_user)):
    ret = await chatbot_agent2.ainvoke(
        input={"user_id": current_user.get("uid"),"messages": [HumanMessage(content=chat_input.question)]},
        config={"configurable": {"thread_id": chat_input.session_id if chat_input.session_id else current_user.get("uid")}},
    )
    messages = ret.get("messages")
    return ChatResponse(answer=messages[-1].content, session_id=chat_input.session_id if chat_input.session_id else current_user.get("uid"))

