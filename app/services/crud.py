from typing import Optional
from fastapi import Response, status, HTTPException
from sqlmodel import Session, select
from app.models.urls import Urls
from app.models.user import User
from app.services.urlshortener import url_shortener
from app.core.config import settings




# url related CRUD operations

async def shorten(url: Urls, db: Session,  user: User):
    """logic for shortening urls"""
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url, Urls.user_id == user.id)).first()
    if url_query:
        return {"status": "success"}
    url.user_id = user.id
    long_url = url.original_url
    short_url = url_shortener.shorten_url(long_url)
    url.Shortened_url = f"{settings.BACKEND_URL}/r/{short_url}"
    db.add(url)
    db.commit()
    return {"status": "success"}

async def get_limit_urls_for_user(db: Session, user: User, limit: int, skip: int):
    url_query = db.exec(select(Urls).where(Urls.user_id == user.id).order_by(Urls.created_at.desc()).limit(limit).offset(skip)).all() # type: ignore
    if not url_query:
        return None
    return url_query

async def get_all_urls_for_user(db: Session, user: User, search: Optional[str]):
    url_query = db.exec(select(Urls).where(Urls.user_id == user.id).filter(Urls.original_url.contains(search))).all() # type: ignore
    if not url_query:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"url does not exists yet pls shorten")
    return url_query

async def updated_url(db: Session, url_id: int, url: Urls):
    url_query = db.get(Urls, url_id)
    url_check = db.exec(select(Urls).where(Urls.original_url == url.original_url)).first()
    if not url_query:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"url with the id {url_id} does not exists")
    if url_check:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"url already exists")
    for field, value in url.model_dump().items():
        setattr(url_query, field, value)
    db.commit()
    db.refresh(url_query)
    return url_query

async def deleted_url(db: Session, url_id: int):
    url_query = db.get(Urls, url_id)
    if not url_query:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"url with the id {url_id} does not exists")
    db.delete(url_query)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

async def redirct_details(url: str, db: Session):
    url_query = db.exec(
        select(Urls).where(Urls.Shortened_url == url)).first()
    return url_query


