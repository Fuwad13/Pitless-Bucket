import asyncio
import json
import os
from typing import Annotated, List

import aiofiles
import chromadb
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

from backend.config import Config
from backend.db.main import async_engine
from backend.db.models import FileChunk, FileInfo, StorageProvider
from backend.storage_provider.factory import get_provider

from .llm import get_model
from .prompts import system_prompt1

chroma_client = chromadb.PersistentClient(path=Config.CHROMADB_PATH)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", api_key=Config.OPENAI_API_KEY
)
vectorstore = Chroma(
    client=chroma_client,
    collection_name="file_content_summary",
    embedding_function=embeddings,
)



memory = MemorySaver()
model = get_model("gemini-2.0-flash")


system_prompt = SystemMessage(
    content=system_prompt1
)


class ChatbotAgentState(AgentState):
    user_id: str


@tool
def get_user_id(state: Annotated[ChatbotAgentState, InjectedState]) -> str:
    """
    Use this tool to get the user_id from the graph state.
    """
    return state["user_id"]

@tool
async def download_file_tool(
    file_id: Annotated[str, "The file ID extracted from document metadata"],
    state: Annotated[ChatbotAgentState, InjectedState]
) -> str:
    """
    Use this tool to download the full content of a file given its file ID.
    Ensures the file belongs to the user.
    """
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
        return f"Error downloading file: {e}"


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
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4, "filter": {"user_id": state["user_id"]}}
    )
    results = retriever.invoke(query)
    return results



tools = [retriever_tool, download_file_tool]

chatbot_agent2 = create_react_agent(
    model=model,
    tools=tools,
    checkpointer=memory,
    state_schema=ChatbotAgentState,
    prompt=system_prompt,
)
