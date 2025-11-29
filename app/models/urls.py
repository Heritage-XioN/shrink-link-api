from datetime import datetime
from typing import Optional
from sqlalchemy import BLOB, TIMESTAMP, Column, String
from sqlmodel import Field, SQLModel, text


# products database model
class Urls(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    Original_url: str = Field(unique=True)
    Shortened_url: str
    clicks: str
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    