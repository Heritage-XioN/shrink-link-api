from datetime import datetime
from typing import List
from pydantic import EmailStr
from sqlmodel import SQLModel



class Urls_base(SQLModel):
    id: int
    original_url: str
    Shortened_url: str
    clicks: int
    created_at: datetime
    class Config:
        from_attributes = True

class Url_Users(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime



class Urls_response(SQLModel):
    id: int
    user_id: int
    original_url: str
    Shortened_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True

class redirct_response(SQLModel):
    message: str

    class Config:
        from_attributes = True

class shortener_response(SQLModel):
    id: int
    user_id: int
    original_url: str
    Shortened_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True