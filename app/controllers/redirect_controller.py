from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.urls import Urls
from app.schemas.urls import redirct_response
from app.core.config import settings

router = APIRouter(
    prefix="/r",
    tags=["redirct"]
)

# route for handling redirect
@router.get("/{url_hash}", status_code=status.HTTP_307_TEMPORARY_REDIRECT, response_model=redirct_response)
async def get_redirect_details(url_hash: str, db: Annotated[Session, Depends(get_session)], res: Response):
    # constructs the full url with url hash from the request
    complete_url = f"{settings.BACKEND_URL}/r/{url_hash}"
    # query the db for the url object
    url_query = db.exec(select(Urls).where(
        Urls.Shortened_url == complete_url)).first()
    # handles error situations where the url object does not exist
    if url_query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    # tracks the current value of clicks
    current_clicks: int = url_query.clicks or 0
    # increments the current value with 1
    increased_count: int = current_clicks + 1 
    # updates the click in the url object with the updated value
    url_query.clicks = increased_count
    # adds commits and refreshes the url object in the db
    db.add(url_query)
    db.commit()
    db.refresh(url_query)
    # gets the original url from the db
    original_url = url_query.original_url
    # pass in the oraginal url to the response header
    res.headers["Location"] = original_url
    return {"message": "suceess"}

