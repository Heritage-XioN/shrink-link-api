from datetime import datetime
from typing import Optional
from pydantic import UUID1
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text


class UserURLLink(SQLModel, table=True):
    user_id: int | None = Field(
        default=None, foreign_key="user.id", primary_key=True)
    url_id: int | None = Field(
        default=None, foreign_key="urls.id", primary_key=True)
    created_at: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
