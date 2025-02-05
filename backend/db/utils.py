from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from backend.db.models import Base
from backend.config import Config

engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))

# Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
