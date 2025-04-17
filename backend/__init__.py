from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.router import auth_router
from backend.db.main import init_db
from backend.file_manager.router import fm_router
from backend.log.logger import get_logger
from backend.ai.vectorstore import init_chromadb
from backend.ai.router import ai_router

logger = get_logger(__name__, Path(__file__).parent / "log" / "app.log")


@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("Server is starting......")
    # await init_db() # uncomment this if there was a database schema change
    # init_chromadb()
    yield
    logger.info("Server is shutting down......")


version = "v1"

app = FastAPI(
    title="Pitless Bucket",
    description="A REST API for Pitless Bucket - Distributed File Storage",
    version=version,
    lifespan=life_span,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pitless-bucket.vercel.app",
        # "http://localhost:3000",
        # "http://localhost:5173",
    ],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(
    fm_router, prefix=f"/api/{version}/file_manager", tags=["file_manager"]
)
app.include_router(ai_router, prefix=f"/api/{version}/ai", tags=["ai"])
