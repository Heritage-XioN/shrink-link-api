from datetime import datetime
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text

from app.models.user import User

class UserURLLink(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    url_id: int = Field(foreign_key="urls.id", primary_key=True)
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
   
    