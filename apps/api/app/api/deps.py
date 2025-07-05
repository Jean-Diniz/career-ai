from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from app.db.session import SessionLocal
from app.db.crud import get_user, get_user_with_relationships
from app.schemas.token import TokenData
from app.core.config import settings
from app.db.models import User as UserTable

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, token_data.username)
    if not user:
        raise credentials_exception
    return user

async def get_current_user_with_relationships(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserTable:
    """
    Retorna o usuário atual com relacionamentos carregados.
    Usado quando precisamos acessar diagnostics e study_trails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_with_relationships(db, token_data.username)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_user_with_relationships(
    current_user: UserTable = Depends(get_current_user_with_relationships),
):
    """
    Retorna o usuário ativo atual com relacionamentos carregados.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user