from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from app.core.security import get_current_user
from app.schemas.user import Get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

# handles getting the logged in user
@router.get("/logged_in", status_code=status.HTTP_200_OK, response_model=Get_current_user)
async def get_logged_in_user(user: Annotated[User, Depends(get_current_user)]):
    # returns a error if user is not logged in
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not authenticated")
    return user
