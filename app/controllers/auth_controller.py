from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import AuthResponse
from app.utils.helpers import verify
from app.schemas.user import User_register_response
from app.utils.helpers import hash


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# route for creating a user
@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=User_register_response)
def create_user(user: User, db: Annotated[Session, Depends(get_session)]):
    hashed_password = hash(user.password)
    user.password = hashed_password
    user_query = db.exec(select(User).where(User.email == user.email)).first()
    if user_query:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"user already exist pls login")
    db.add(user)
    db.commit()
    return {"status": "success"}


# route for logging in
# login_credentials must be sent as form data not json
# if you want to send as json then use the LoginAuth defined in the app.schema.auth module
@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthResponse)
def login(login_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_session)]):
    user_query = db.exec(select(User).where(
        User.email == login_credentials.username)).first()
    # checks if the user exists
    if not user_query:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Invalid credentials")
    # if the exist then check if they provided the correct password
    if not verify(login_credentials.password, user_query.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Invalid credentials")
    # if all statement above evaluate withot exceptions then create auth token
    access_token = create_access_token(data={"user_id": user_query.id})
    return {"status": "success", "access_token": access_token, "token_type": "Bearer"}

