from typing import Optional
from fastapi import Response, status, HTTPException
from sqlmodel import Session, select
from app.models.urls import Urls
from app.models.user import User
from app.services.urlshortener import url_shortener
from app.core.config import settings




# url related CRUD operations

async def shorten(url: Urls, db: Session,  user: User):
    # gets the url object from the database
    url_query = db.exec(select(Urls).where(
        Urls.original_url == url.original_url, Urls.user_id == user.id)).first()
    # if the url already exist just return success instead of an error trying to create another one
    if url_query:
        return {"status": "success"}
    # adds the user id of the logged in user shortening the url
    url.user_id = user.id
    # gets the long url
    long_url = url.original_url
    # shortens the url
    short_hash = url_shortener.shorten_url(long_url)
    # constructs the short url
    Shortened_url = f"{settings.BACKEND_URL}/r/{short_hash}"
    # query db for collision detection
    short_url_query = db.exec(select(Urls).where(
        Urls.Shortened_url == Shortened_url, Urls.user_id == user.id)).first()
    # handles resolving url hash collision
    collision_attempt = 0
    while short_url_query:
        # Collision Increment counter and (salt)
        collision_attempt += 1
        # Resolve the collision by salting
        short_hash = url_shortener.resolve_collision(
            url.original_url, 
            collision_attempt
        )
        # Set a maximum loop limit to prevent infinite loops in extreme edge cases
        if collision_attempt > 100:
            # Handle catastrophic failure 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="High collision rate detected. Cannot generate a unique short URL.")
        # construct shortened url with salted hash
        Shortened_url = f"{settings.BACKEND_URL}/r/{short_hash}"
        # query db to verify collision status
        short_url_query = db.exec(select(Urls).where(
        Urls.Shortened_url == Shortened_url, Urls.user_id == user.id)).first()
    # if collision is resolved or no collision at all then add the shortened url to the url object 
    url.Shortened_url = Shortened_url
    # adds, commits, and refreshes the url object in the db
    db.add(url)
    db.commit()
    db.refresh(url)
    return {"status": "success"}

# handles getting urls based on the set limit
async def get_limit_urls_for_user(db: Session, user: User, limit: int, skip: int):
    # gets the url object
    url_query = db.exec(select(Urls).where(Urls.user_id == user.id).order_by(Urls.created_at.desc()).limit(limit).offset(skip)).all()  # type: ignore
    # returns 404 not found and a message if the url does not exist
    if not url_query:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"url does not exists yet pls shorten")
    return url_query

# handles getting all the urls
async def get_all_urls_for_user(db: Session, user: User, search: Optional[str]):
    # gets the url object
    url_query = db.exec(select(Urls).where(Urls.user_id == user.id).filter(Urls.original_url.contains(search))).all() # type: ignore
    # returns 404 not found and a message if the url does not exist
    if not url_query:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"url does not exists yet pls shorten")
    return url_query

async def updated_url(db: Session, url_id: int, url: Urls):
    # handles getting the url object by id
    url_query = db.get(Urls, url_id)
    # handles getting the url object by using the original url
    url_check = db.exec(select(Urls).where(Urls.original_url == url.original_url)).first()
    # returns 404 not found and a message if the url does not exist
    if not url_query:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"url with the id {url_id} does not exists")
    # handles if the updated url already exist in the db
    if url_check:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"url already exists")
    # handles updating the url in the db
    for field, value in url.model_dump().items():
        setattr(url_query, field, value)
    db.commit()
    db.refresh(url_query)
    return url_query

# handles deleting the url in the db 
async def deleted_url(db: Session, url_id: int):
    # handles getting the url object by id
    url_query = db.get(Urls, url_id)
    # returns 404 not found and a message if the url does not exist
    if not url_query:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"url with the id {url_id} does not exists")
    # handles deleting the url object from the db
    db.delete(url_query)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# handles sending the redirect details
async def redirct_details(url: str, db: Session):
    url_query = db.exec(
        select(Urls).where(Urls.Shortened_url == url)).first()
    return url_query


