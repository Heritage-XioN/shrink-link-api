from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends,status
from sqlmodel import Session
from app.core.crud import deleted_url, get_all_urls_for_user, get_limit_urls_for_user, shorten, updated_url
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.urls import Urls
from app.schemas.urls import Urls_base, Urls_response, shortener_response
from app.models.user import User

router = APIRouter(
    prefix="/url",
    tags=["url"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=shortener_response)
async def shorten_url(url: Urls, db: Annotated[Session, Depends(get_session)],  user: Annotated[User, Depends(get_current_user)]):
    return await shorten(url, db, user)

@router.get("/", status_code=status.HTTP_200_OK, response_model=Optional[List[Urls_base]])
async def get_limit_url(db: Annotated[Session, Depends(get_session)],  user: Annotated[User, Depends(get_current_user)],  limit: int = 3, skip: int = 0):
    return await get_limit_urls_for_user(db,user,limit,skip)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[Urls_base])
async def get_all_url(db: Annotated[Session, Depends(get_session)],  user: Annotated[User, Depends(get_current_user)], search: Optional[str] = ""):
    return await get_all_urls_for_user(db,user,search)


@router.put("/{url_id}", status_code=status.HTTP_200_OK, response_model=Urls_response)
async def update_url(url_id: int, url: Urls, db: Annotated[Session, Depends(get_session)], user: Annotated[User, Depends(get_current_user)]):
    return await updated_url(db, url_id, url)

@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(url_id: int, db: Annotated[Session, Depends(get_session)], user: Annotated[User, Depends(get_current_user)]):
    return  await deleted_url(db, url_id)

