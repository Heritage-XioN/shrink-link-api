from logging import config
from typing import Annotated, List
from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session, select
from app.core.crud import get_url_with_users, get_urls, redirct_details, shorten
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.urls import Urls
from app.schemas.urls import Urls_response, redirct_response
from app.models.user import User
from app.core.config import settings

router = APIRouter(
    prefix="/r",
    tags=["redirct"]
)

@router.get("/{short_url}", status_code=status.HTTP_308_PERMANENT_REDIRECT, response_model=redirct_response)
async def get_redirect_details(short_url: str, db: Annotated[Session, Depends(get_session)], res: Response):
    complete_url = f"{settings.BACKEND_URL}/r/{short_url}"
    url_query = db.exec(select(Urls).where(
        Urls.Shortened_url == complete_url)).first()
    original_url = url_query.original_url # type: ignore
    res.headers["Location"] = original_url
    return {"message": "suceess"}

