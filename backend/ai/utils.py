from langchain_community.document_loaders import PyPDFLoader

from .agents import summarizer_agent


def summarize_file_content(file_path: str, firebase_uid: str):
    """
    Summarize the content using a language model.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    for doc in documents:
        pass