from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.main import init_db
from backend.log.logger import get_logger
from backend.auth.router import auth_router

from backend.file_manager.router import fm_router

logger = get_logger(__name__, Path(__file__).parent / "log" / "app.log")


@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("Server is starting......")
    await init_db()
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
        "*"
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
