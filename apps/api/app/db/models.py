from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)
    linkedin_url = Column(String, nullable=False)
    
    # Relacionamentos
    diagnostics = relationship("Diagnostic", back_populates="user", lazy="joined")
    study_trails = relationship("StudyTrail", back_populates="user", lazy="joined")

class Diagnostic(Base):
    __tablename__ = "diagnostics"

    id = Column(Integer, primary_key=True, index=True)
    diagnostic = Column(Text, nullable=False)
    linkedin_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relacionamentos
    user = relationship("User", back_populates="diagnostics")

class StudyTrail(Base):
    __tablename__ = "study_trails"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)  # JSON da trilha completa
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relacionamentos
    user = relationship("User", back_populates="study_trails")