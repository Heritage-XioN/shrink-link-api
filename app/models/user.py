from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr
from sqlalchemy import TIMESTAMP, Column, String
from sqlmodel import Field, Relationship, SQLModel, text
from app.models.urls import Urls
from app.models.user_url_link import UserURLLink


# user database model
class User(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column( primary_key=True,
        nullable=False, server_default=text("gen_random_uuid()")))
    email: EmailStr = Field(unique=True)
    password: str
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    
    items: List["Urls"] = Relationship(back_populates="Users", link_model= "UserURLLink")
    items_link: List["UserURLLink"] = Relationship(back_populates="Users")
