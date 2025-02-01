from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Double
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # password_hash = Column(String, nullable=False)  # Secure storage recommended
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    drives = relationship("GoogleDrive", back_populates="user")
    files = relationship("File", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, created_at={self.created_at})>"


class GoogleDrive(Base):
    __tablename__ = "google_drive"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    # refresh_token = Column(String, nullable=False)
    creds = Column(String, nullable=False)  # JSON string
    used_space = Column(Integer, default=0)  # In bytes
    total_space = Column(Integer, nullable=False)  # Google Drive limit

    user = relationship("User", back_populates="drives")
    # file_storages = relationship("FileStorage", back_populates="drives")

    def __repr__(self):
        return f"<GoogleDrive(user_id={self.user_id}, email={self.email}, used_space={self.used_space}, total_space={self.total_space})>"


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # In bytes
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    user = relationship("User", back_populates="files")
