from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, FastAPI, Response, status, HTTPException
from sqlalchemy import true
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
from app.core.config import settings




async def user_url_linker(url: Urls, db: Session, user: User):
    """logic for linking the user and the url. this facilitates the many to many relationship"""
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    user_url_link = UserURLLink(
        user_id=user.id, url_id=url_query.id, created_at=None)  # type: ignore
    db.add(user_url_link)
    db.commit()
    return True

async def verify_user_url_link(url: Urls, db: Session, user: User):
    """this logic verifies if the user is linked to a url"""
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    association_query = db.exec(select(UserURLLink).where(UserURLLink.user_id == user.id,
                                                          UserURLLink.url_id == url_query.id)).first()# pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
    if association_query:
        return association_query
    return False

# url related CRUD operations

async def shorten(url: Urls, db: Session,  user: User):
    """logic for shortening urls"""
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    if url_query:
        if not await verify_user_url_link(url, db, user):
            await user_url_linker(url_query, db, user)
        return {"message": "success"}

    long_url = url.original_url
    short_url = url_shortener.shorten_url(long_url)
    url.Shortened_url = f"{settings.BACKEND_URL}/r/{short_url}"
    print(url)
    db.add(url)
    db.commit()
    await user_url_linker(url, db, user)
    db.refresh(url)
    return {"message": "success"}


async def get_urls(db:Session):
    """logic for getting all urls and all associated users eho shortened them"""
    url_query = db.exec(
        select(Urls).options(selectinload(Urls.users))).all() # type: ignore
    return url_query

async def get_url_with_users(id: int, db: Session):
    """logic for getting a url and all associated users who shortened the Oringinal url"""
    url_query = db.exec(select(Urls).where(Urls.id == id).options(selectinload(Urls.users))).first() # type: ignore
    return url_query

async def get_all_urls_for_user():
    return

async def redirct_details(url: str, db: Session):
    url_query = db.exec(
        select(Urls).where(Urls.Shortened_url == url)).first()
    return url_query


# user related CRUD operations

async def get_users(db:Session):
    """logic for getting all user and all associated urls which they shortened"""
    user_query = db.exec(
        select(User).options(selectinload(User.urls))).all() # type: ignore
    return user_query

async def get_user_with_urls(id: int, db: Session):
    """logic for getting a user and all associated urls which they shortened"""
    user_query = db.exec(select(User).where(User.id == id).options(selectinload(User.urls))).first() # type: ignore
    return user_query


