from typing import Annotated, List

import chromadb
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from backend.config import Config
from backend.db.main import get_session

from .llm import get_model

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
    content=(
        "You are a helpful assistant for the Pitless Bucket System name Pitless Bucket Bot.\n"
        "Your role is to assist users and reply to their queries. You have access to the user's files summarys stored in a vectorstore.\n"
        "- You can use the retriever_tool to get the relevant document summaries from the vectorstore.\n"
        "- You may want to refine the query before using the retriever_tool.\n"
        "- If you don't know the answer and there is no relevant document in the vectorstore, you can say that you don't know about it.\n"
        "- You can use the retriever_tool to get the relevant documents from the vectorstore if the asked question doesn't have any context in the chat history."
        "then you can analyze the retrieved documents and answer the user's question.\n"
        " - Take the chat history into account when answering the user's question.\n"
        "You can also ask clarifying questions to the user if needed."
        "Example 1: \n"
        "User: When is my next chemistry exam?\n"
        "Bot: Your next chemistry exam is on 2023-10-15. Reference: schedule_file_name_from_metadata\n"
        "Example 2: \n"
        "User: Summarize my resume\n"
        "Bot: Sorry, I couldn't find any file that have your resume. You can upload it and I'll summarize it for you\n"
    )
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
def retriever_tool(
    query: Annotated[str, "User's query (possibly refined by the agent)"],
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



tools = [retriever_tool]

chatbot_agent = create_react_agent(
    model=model,
    tools=tools,
    checkpointer=memory,
    state_schema=ChatbotAgentState,
    prompt=system_prompt,
)
