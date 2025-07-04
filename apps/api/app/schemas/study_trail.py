from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StudyTrailCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content: str  # JSON da trilha completa
    user_id: int


class StudyTrail(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 