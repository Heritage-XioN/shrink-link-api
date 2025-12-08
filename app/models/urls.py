from datetime import datetime
from typing import Optional
from sqlalchemy import TIMESTAMP, Column, Integer
from sqlmodel import Field, SQLModel, text



# Url database model
class Urls(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True, nullable=False, index=True))
    user_id: Optional[int] = Field(foreign_key="user.id", ondelete="CASCADE", nullable=False)
    original_url: str 
    Shortened_url: str
    clicks: Optional[int] = Field(sa_column=Column(Integer, server_default=text("0"), nullable=False))
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    