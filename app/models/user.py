from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from sqlalchemy import TIMESTAMP, Column, String
from sqlmodel import Field, SQLModel, text


# user database model
class User(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column( primary_key=True,
        nullable=False, server_default=text("gen_random_uuid()")))
    email: EmailStr = Field(unique=True)
    password: str
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
