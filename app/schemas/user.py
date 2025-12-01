from datetime import datetime
from typing import List
from pydantic import EmailStr
from sqlmodel import SQLModel



# schema for getting a user
class UserBase(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

class User_Urls(SQLModel):
    id: int
    original_url: str
    Shortened_url: str


# schema for the response for the of the register user route
class UserResponse(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime
    urls: List[User_Urls] = []

    class Config:
        from_attributes = True

class User_register_response(SQLModel):
    status: str

    class Config:
        from_attributes = True


class Get_current_user(UserBase):
    pass
