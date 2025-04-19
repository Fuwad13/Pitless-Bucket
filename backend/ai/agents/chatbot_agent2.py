import asyncio
import datetime
import json
import os
from pathlib import Path
from typing import Annotated, List

import aiofiles
import chromadb
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.config import settings
from backend.db.main import async_engine
from backend.db.models import FileChunk, FileInfo, StorageProvider, User
from backend.log.logger import get_logger
from backend.storage_provider.factory import get_provider

from .llm import get_model
from .prompts import (
    CHATBOT_AGENT_PROMPT,
    CHATBOT_AGENT_PROMPT2,
    CHATBOT_AGENT_PROMPT3,
    CHATBOT_AGENT_PROMPT_GPT,
)

logger = get_logger(__name__, Path(settings.LOG_FILE_PATH))

chroma_client = chromadb.PersistentClient(path=settings.CHROMADB_PATH)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY
)
vectorstore = Chroma(
    client=chroma_client,
    collection_name="file_content_summary",
    embedding_function=embeddings,
)


memory = MemorySaver()
model = get_model("gemini-2.0-flash")


system_prompt = SystemMessage(content=CHATBOT_AGENT_PROMPT_GPT)


class ChatbotAgentState(AgentState):
    user_id: str


@tool
def get_user_id(state: Annotated[ChatbotAgentState, InjectedState]) -> str:
    """
    Use this tool to get the user_id from the graph state.
    """
    return state["user_id"]


@tool
def get_datetime() -> str:
    """
    Use this tool to get the current datetime.
    """
    return str(datetime.datetime.now())


@tool
async def get_user_info(state: Annotated[ChatbotAgentState, InjectedState]) -> str:
    """
    Use this tool to get the user's information from the database.
    """
    logger.debug(f"Calling get_user_info tool user_id {state['user_id']}")
    user_id = state["user_id"]
    try:
        async with AsyncSession(async_engine) as session:
            stmt = select(User).where(User.firebase_uid == user_id)
            result = (await session.exec(stmt)).first()
            if not result:
                return "User not found"
            return result.model_dump(mode="json")
    except Exception as e:
        return f"Error getting user info: {e}"


cache = TTLCache(maxsize=100, ttl=1800)


def cache_key(file_id, state):
    return hashkey(state["user_id"], file_id)


# @cached(cache, key=cache_key)
@tool
async def download_file_tool(
    file_id: Annotated[str, "The file ID extracted from document metadata"],
    state: Annotated[ChatbotAgentState, InjectedState],
) -> str:
    """
    Use this tool to download the full content of a file given its file ID.
    Use this tool only for pdf, docx, txt and other readable files only.
    Ensures the file belongs to the user.
    """
    logger.debug(f"Calling download_file_tool with file_id {file_id}")
    user_id = state["user_id"]

    try:
        async with AsyncSession(async_engine) as session:
            stmt = select(FileInfo).where(FileInfo.uid == file_id)
            result = (await session.exec(stmt)).first()
            if not result:
                return "File not found"
            if result.firebase_uid != user_id:
                return "Unauthorized access to file"

            stmt = select(FileChunk).where(FileChunk.file_id == file_id)
            chunks = await session.exec(stmt)
            if not chunks:
                return "File has no chunks"
            async with aiofiles.tempfile.NamedTemporaryFile(
                "wb", delete=False, delete_on_close=True
            ) as temp_file:
                for chunk in chunks:
                    stmt = select(StorageProvider).where(
                        StorageProvider.uid == chunk.provider_id
                    )
                    res_sp = (await session.exec(stmt)).first()
                    provider = get_provider(
                        res_sp.provider_name,
                        credentials=json.loads(res_sp.creds),
                    )
                    chunk_path = await asyncio.to_thread(
                        provider.download_chunk, chunk.provider_file_id
                    )
                    async with aiofiles.open(chunk_path, "rb") as f:
                        await temp_file.write(await f.read())
                    os.remove(chunk_path)

                if result.extension == "pdf":
                    loader = PyPDFLoader(temp_file.name)
                elif result.extension in ["doc", "docx"]:
                    loader = Docx2txtLoader(temp_file.name)
                elif result.extension == "txt":
                    loader = TextLoader(temp_file.name)
                else:
                    raise ValueError(f"Unsupported file type: {result.extension}")
                documents = await loader.aload()
                return "\n".join([doc.page_content for doc in documents])

    except Exception as e:
        print(e)
        return f"Error downloading file: {e}"


@tool
async def get_file_list(
    state: Annotated[ChatbotAgentState, InjectedState],
) -> List[dict]:
    """
    Use this tool to get the list of files belonging to the user.
    """
    logger.debug(f"Calling get_file_list tool user_id {state['user_id']}")
    user_id = state["user_id"]
    try:
        async with AsyncSession(async_engine) as session:
            stmt = select(FileInfo).where(FileInfo.firebase_uid == user_id)
            results = await session.exec(stmt)
            files = results.all()
            if not files:
                return []
            return [file.model_dump(mode="json") for file in files]
    except Exception as e:
        return f"Error retrieving file list: {e}"


@tool
def retriever_tool(
    query: Annotated[str, "User's query (refined by the agent)"],
    state: Annotated[ChatbotAgentState, InjectedState],
) -> List[Document]:
    """
    Use this tool to retrieve relevant documents from the vectorstore.
    You can use the retriever_tool to get the relevant documents from the vectorstore.
    You can refine the query to get better retrival before using the retriever_tool.
    """
    logger.debug(f"Calling retriever_tool with query: {query}")
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4, "filter": {"user_id": state["user_id"]}}
    )
    results = retriever.invoke(query)
    return results


tools = [retriever_tool, download_file_tool, get_user_info, get_file_list, get_datetime]

chatbot_agent2 = create_react_agent(
    model=model,
    tools=tools,
    checkpointer=memory,
    state_schema=ChatbotAgentState,
    prompt=system_prompt,
)
