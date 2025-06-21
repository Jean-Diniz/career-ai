from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate
from app.db.crud import get_user, create_user
from app.api.deps import get_db, get_current_active_user
from app.db.models import User as UserTable

router = APIRouter()

@router.post(
    "/users/", response_model=User, status_code=status.HTTP_201_CREATED
)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    if get_user(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if user_in.email and db.query(UserTable).filter(UserTable.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db, user_in)

@router.get(
    "/users/me/", response_model=User
)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user