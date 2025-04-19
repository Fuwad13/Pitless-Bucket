from functools import cache

from langchain_google_genai import ChatGoogleGenerativeAI

from backend.config import settings


@cache
def get_model(model_name: str):
    """
    Get llm model by name
    """
    # TODO: Add support for other models
    if model_name == "gemini-2.0-flash":
        return ChatGoogleGenerativeAI(model=model_name, api_key=settings.GOOGLE_API_KEY)
    else:
        raise ValueError(f"Model {model_name} is not supported yet or not available.")
