import chromadb

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from backend.config import Config

EMBEDDING_MODEL = "text-embedding-3-small"

def init_chromadb():
    chroma_client = chromadb.PersistentClient(path=Config.CHROMADB_PATH)
    embedding_function = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=Config.OPENAI_API_KEY)
    vectorstore = Chroma(
        client=chroma_client,
        collection_name="file_content_summary",
        embedding_function=embedding_function,
        create_collection_if_not_exists=True
    )

