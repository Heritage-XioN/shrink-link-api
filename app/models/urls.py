from datetime import datetime
from typing import List, Optional
from sqlalchemy import BLOB, TIMESTAMP, Column, String
from sqlmodel import Field, Relationship, SQLModel, text
from app.models.user_url_link import UserURLLink


# Url database model
class Urls(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    original_url: str = Field(unique=True)
    Shortened_url: Optional[str]
    clicks: Optional[str]
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    
    users: List["Urls"] = Relationship(back_populates="Urls", link_model= "UserURLLink")
    users_link: List["UserURLLink"] = Relationship(back_populates="Urls")