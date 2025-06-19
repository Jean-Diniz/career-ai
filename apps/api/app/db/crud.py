from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from app.db.models import User as UserTable
from app.schemas.user import UserCreate, UserInDB
from app.schemas.token import TokenData

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


def create_user(db: Session, user_in: UserCreate) -> UserInDB:
    hashed = get_password_hash(user_in.password)
    db_user = UserTable(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed,
        disabled=False,
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