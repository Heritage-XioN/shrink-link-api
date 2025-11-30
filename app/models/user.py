from datetime import datetime
from typing import List, Optional
from pydantic import UUID1, EmailStr
from sqlalchemy import TIMESTAMP, Column, Integer, String, Uuid
from sqlmodel import Field, Relationship, SQLModel, text
from app.models.user_url_link import UserURLLink


# user database model
class User(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True,
                                               nullable=False))
    email: EmailStr = Field(unique=True)
    password: str
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))

    urls: List["Urls"] = Relationship(  # type: ignore
        back_populates="users", link_model=UserURLLink)
    # urls_link: List["UserURLLink"] = Relationship(back_populates="User")
