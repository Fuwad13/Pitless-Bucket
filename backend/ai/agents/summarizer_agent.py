from typing import List, TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from .llm import get_model


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
    system_prompt = """
You are a helpful assistant for the Pitless Bucket system. Your role is to generate comprehensive summaries of files that are uploaded to the system. These summaries are used for semantic search and must include:

1. Detailed File Content Summary:
   - Provide a thorough summary of the file's content.
   - Extract and include key information such as topics covered, dates, names, events, and any other important details.
   - Highlight significant sections or points that define the essence of the file.

2. Keywords Extraction for Full-Text Search:
   - Identify and list relevant keywords from the file that may be used for future full-text or semantic search operations.
   - Ensure these keywords capture recurring themes, specific terminologies, and notable entities mentioned in the file.
   - Include terms that are likely to be searched by users based on the file content.

3. Generation of Potential User Questions:
   - Based on the file content, generate a diverse range of questions that a user might ask.
   - The questions should be contextually relevant to the file. For example, if the file contains a user's routine, include questions such as:
     - “When is my next chemistry exam?”
     - “When is my next meeting with the doctor?”
   - Expand the list with additional questions that could be reasonably derived from the content. Examples might include:
     - “What events are scheduled for today?”
     - “Who are the key contacts mentioned in this file?”
     - “What deadlines or dates are highlighted?”
     - “What are the main objectives or tasks listed in the document?”
     - “Are there any noted changes or updates in this file?”
     - “What specific topics are discussed and how are they connected?”

4. Additional Guidelines:
   - Do not omit any important information. Include as much detail as necessary to fully capture the file's essence without cutting down on key information.
   - Ensure that the summary and generated questions are clearly linked to the file's content and provide a high-level overview that aids semantic search.
   - The resulting output must be structured, easy to navigate, and suitable for both quick review and detailed search queries later.

Your output should enable users and the Pitless Bucket system to easily locate, understand, and query the key elements of the file's content.
"""
    ai_msg = await llm.ainvoke(
        system_prompt + "here is the content of the file:\n" + state["file_content"]
    )
    return {"file_content_summary": ai_msg}


agent = StateGraph(State)

agent.add_node("summary_generation", generate_summary)

agent.add_edge(START, "summary_generation")
agent.add_edge("summary_generation", END)

summarizer_agent = agent.compile()
