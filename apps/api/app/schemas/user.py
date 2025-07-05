from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    linkedin_url: str

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str
    linkedin_url: str

class DiagnosticBase(BaseModel):
    id: int
    diagnostic: str
    linkedin_url: str
    created_at: datetime
    user_id: Optional[int] = None

class StudyTrailBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content: str
    user_id: int
    created_at: datetime

class UserWithRelationships(User):
    """
    Schema para usuário com relacionamentos carregados.
    Usado quando precisamos acessar diagnostics e study_trails.
    """
    diagnostics: List[DiagnosticBase] = []
    study_trails: List[StudyTrailBase] = []

    class Config:
        from_attributes = True