from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Secure storage recommended

    drives = relationship("GoogleDrive", back_populates="user")
    files = relationship("File", back_populates="user")

class GoogleDrive(Base):
    __tablename__ = 'google_drive'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    drive_name = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)  # Encrypt before storing
    used_space = Column(Integer, default=0)  # In bytes
    total_space = Column(Integer, nullable=False)  # Google Drive limit

    user = relationship("User", back_populates="drives")
    file_storages = relationship("FileStorage", back_populates="drive")

class File(Base):
    __tablename__ = 'file'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)  # In bytes
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="files")
    storages = relationship("FileStorage", back_populates="file")

class FileStorage(Base):
    __tablename__ = 'file_storage'
    
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('file.id'), nullable=False)
    drive_id = Column(Integer, ForeignKey('google_drive.id'), nullable=False)
    drive_file_id = Column(String, nullable=False)  # File ID in Google Drive
    is_primary = Column(Boolean, default=False)  # Indicates main storage location

    file = relationship("File", back_populates="storages")
    drive = relationship("GoogleDrive", back_populates="file_storages")
