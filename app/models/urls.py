
from datetime import datetime
from typing import List, Optional
from sqlalchemy import BLOB, INTEGER, TIMESTAMP, Column, Integer, String, true
from sqlmodel import Field, Relationship, SQLModel, text
#from app.models.user_url_link import UserURLLink


# Url database model
class Urls(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer,
                                               primary_key=True, nullable=False, index=True))
    user_id: Optional[int] = Field(foreign_key="user.id", ondelete="CASCADE", nullable=False)
    original_url: str = Field(unique=True)
    Shortened_url: str
    clicks: Optional[int] = Field(sa_column=Column(Integer, default=0, nullable=False))
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    
    #TODO: implement proper type safety with annonated
    # users: List["User"] = Relationship(  # type: ignore
    #     back_populates="urls", link_model=UserURLLink)
    # users_link: List["UserURLLink"] = Relationship(back_populates="urls")
