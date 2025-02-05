from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.auth.routes import auth_router
from backend.logs.logger import get_logger
from backend.db.main import init_db

logger = get_logger(
    __name__, Path(__file__).parent / "logs" / "app.log"
)  # check if it is working


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

app.include_router(auth_router, prefix=f"/api/{version}", tags=["auth"])
