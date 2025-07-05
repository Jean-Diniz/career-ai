from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from app.db.models import User as UserTable
from app.schemas.user import UserCreate, UserInDB
from app.schemas.token import TokenData
from app.db.models import Diagnostic as DiagnosticTable, StudyTrail as StudyTrailTable
from app.schemas.study_trail import StudyTrailCreate, StudyTrail

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(db: Session, username: str) -> UserInDB | None:
    db_user = db.query(UserTable).filter(UserTable.username == username).first()
    if not db_user:
        return None
    return UserInDB(**db_user.__dict__)

def get_user_with_relationships(db: Session, username: str) -> UserTable | None:
    """
    Retorna o usuário com relacionamentos carregados (objeto SQLAlchemy).
    Usado quando precisamos acessar diagnostics e study_trails.
    """
    return db.query(UserTable).filter(UserTable.username == username).first()

def create_diagnostic(db: Session, diagnostic: str, linkedin_url: str, user_id: int = None):
    db_diagnostic = DiagnosticTable(
        diagnostic=diagnostic,
        linkedin_url=linkedin_url,
        user_id=user_id
    )
    db.add(db_diagnostic)
    db.commit()
    db.refresh(db_diagnostic)

    return { "diagnostic": diagnostic, "linkedin_url": linkedin_url, "user_id": user_id}

def create_study_trail(db: Session, study_trail: StudyTrailCreate) -> StudyTrail:
    db_study_trail = StudyTrailTable(
        title=study_trail.title,
        description=study_trail.description,
        content=study_trail.content,
        user_id=study_trail.user_id
    )
    db.add(db_study_trail)
    db.commit()
    db.refresh(db_study_trail)
    return StudyTrail(**db_study_trail.__dict__)

def get_study_trails_by_user(db: Session, user_id: int) -> list[StudyTrail]:
    db_trails = db.query(StudyTrailTable).filter(StudyTrailTable.user_id == user_id).all()
    return [StudyTrail(**trail.__dict__) for trail in db_trails]

def get_study_trail(db: Session, trail_id: int) -> StudyTrail | None:
    db_trail = db.query(StudyTrailTable).filter(StudyTrailTable.id == trail_id).first()
    if not db_trail:
        return None
    return StudyTrail(**db_trail.__dict__)

def create_user(db: Session, user_in: UserCreate) -> UserInDB:
    hashed = get_password_hash(user_in.password)
    db_user = UserTable(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed,
        disabled=False,
        linkedin_url=user_in.linkedin_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserInDB(**db_user.__dict__)


def authenticate_user(db: Session, username: str, password: str) -> UserInDB | bool:
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)