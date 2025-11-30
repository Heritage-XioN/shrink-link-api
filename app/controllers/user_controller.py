from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from app.core.crud import get_user_with_urls, get_users
from app.core.database import get_session
from app.core.security import get_current_user
from app.schemas.user import Get_current_user, UserResponse
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.get("/logged_in", status_code=status.HTTP_200_OK, response_model=Get_current_user)
async def get_logged_in_user(user: Annotated[User, Depends(get_current_user)]):
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not authenticated")
    return user

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(db: Annotated[Session, Depends(get_session)]):
    return  await get_users(db)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_id: int, db: Annotated[Session, Depends(get_session)]):
    return  await get_user_with_urls(user_id, db)