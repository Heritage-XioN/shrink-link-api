from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, FastAPI, Response, status, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.urls import Urls
from app.models.user_url_link import UserURLLink
from app.schemas.urls import Urls_response
from app.schemas.user import Get_current_user, UserResponse
from app.models.user import User
from app.utils.helpers import hash
from app.services.urlshortener import url_shortener


async def shorten(url: Urls, db: Session,  user: User):
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    if url_query:
        print(url_query)
        if await user_url_linker(url, db, user):
            return (url_query, await user_url_linker(url_query, db, user))

    long_url = url.original_url
    short_url = url_shortener.shorten_url(long_url)
    url.Shortened_url = short_url
    db.add(url)
    db.commit()
    relationship = await user_url_linker(url, db, user)
    db.refresh(url)
    return (url, relationship)


async def user_url_linker(url: Urls, db: Session, user: User):
    print("url query",url)
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url)).first()
    print("url query after",url_query)
    association_query = db.exec(select(UserURLLink).where(UserURLLink.user_id == user.id,
                                                          UserURLLink.url_id == url_query.id)).first()# pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
    if association_query:
        return association_query
    user_url_link = UserURLLink(
        user_id=user.id, url_id=url_query.id, created_at=None)  # type: ignore
    db.add(user_url_link)
    db.commit()
    db.refresh(user_url_link)
    return user_url_link
