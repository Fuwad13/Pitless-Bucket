from typing import List, TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


from .llm import get_model
from .prompts import SUMMARIZER_PROMPT

class ContentSummary(BaseModel):
    file_content_keywords: List[str] = Field(
        ...,
        description="Keywords from the file",
    )
    file_content_summary: str = Field(
        ...,
        description="File content summary with key information",
    )
    user_questions: List[str] = Field(
        ...,
        description="Questions that the user might ask about the file",
    )


class State(TypedDict):
    file_id: str
    file_name: str
    file_size: int
    file_extension: str
    file_type: str
    file_content: str
    file_content_summary: ContentSummary


async def generate_summary(state: State):
    """
    Generate the summary of the file
    """
    llm = get_model(model_name="gemini-2.0-flash")
    llm = llm.with_structured_output(ContentSummary)
    system_prompt = SUMMARIZER_PROMPT
    ai_msg = await llm.ainvoke(
        system_prompt + "here is the content of the file:\n" + state["file_content"]
    )
    return {"file_content_summary": ai_msg}


agent = StateGraph(State)

agent.add_node("summary_generation", generate_summary)

agent.add_edge(START, "summary_generation")
agent.add_edge("summary_generation", END)

summarizer_agent = agent.compile()
