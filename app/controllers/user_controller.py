from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, FastAPI, Response, status, HTTPException
from sqlmodel import Session, select
from app.core.crud import get_urls, get_user_with_urls, get_users, shorten
from app.core.database import get_session
from app.core.security import get_current_user
from app.models import user
from app.models.urls import Urls
from app.models.user_url_link import UserURLLink
from app.schemas.urls import Urls_response
from app.schemas.user import Get_current_user, UserResponse
from app.models.user import User
from app.utils.helpers import hash
from app.services.urlshortener import url_shortener



router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=Get_current_user)
async def get_logged_in_user(user: Annotated[User, Depends(get_current_user)]):
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not authenticated")
    return user

@router.get("/user", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(db: Annotated[Session, Depends(get_session)]):
    return  await get_users(db)

@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_id, db: Annotated[Session, Depends(get_session)]):
    return  await get_user_with_urls(user_id, db)