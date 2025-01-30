from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utc)

    # Relationships
    drive_accounts = relationship("DriveAccount", back_populates="user")
