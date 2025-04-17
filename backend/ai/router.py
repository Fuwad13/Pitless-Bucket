from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from redis import asyncio as aioredis
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.auth.dependencies import get_current_user
from backend.db.main import get_session
from backend.log.logger import get_logger
from .agents import chatbot_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import InjectedToolArg


logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")

ai_router = APIRouter()

@ai_router.get("/invoke")
async def agent_invoke(q: str):
    ret = await chatbot_agent.ainvoke(
        input={"user_id": "6OJvZ9a5FFWGvTHsuxTMWjVfkOj2", "messages": [HumanMessage(content=q)]},
        config={"configurable": {"thread_id": "user_id_here"}},
    )
    return ret

