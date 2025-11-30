from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, FastAPI, Response, status, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.urls import Urls
from app.models.user_url_link import UserURLLink
from app.schemas.urls import Urls_response
from app.schemas.user import Get_current_user, UserResponse
from app.models.user import User
from app.utils.helpers import hash
from app.services.urlshortener import url_shortener


async def verify_user_url_link(url: Urls, db: Session, user: User):
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    association_query = db.exec(select(UserURLLink).where(UserURLLink.user_id == user.id,
                                                          UserURLLink.url_id == url_query.id)).first()# pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
    if association_query:
        return association_query
    return False

async def shorten(url: Urls, db: Session,  user: User):
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    if url_query:
        if not await verify_user_url_link(url, db, user):
            await user_url_linker(url_query, db, user)
        return url_query

    long_url = url.original_url
    short_url = url_shortener.shorten_url(long_url)
    url.Shortened_url = short_url
    db.add(url)
    db.commit()
    relationship = await user_url_linker(url, db, user)
    db.refresh(url)
    return (url, relationship)


async def user_url_linker(url: Urls, db: Session, user: User):
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    user_url_link = UserURLLink(
        user_id=user.id, url_id=url_query.id, created_at=None)  # type: ignore
    db.add(user_url_link)
    db.commit()
    db.refresh(user_url_link)
    return user_url_link

async def get_urls(db:Session):
    url_query = db.exec(
        select(Urls).options(selectinload(Urls.users))).all() # type: ignore
    return url_query

async def get_users(db:Session):
    user_query = db.exec(
        select(User).options(selectinload(User.urls))).all() # type: ignore
    return user_query

async def get_user_url():
    return
