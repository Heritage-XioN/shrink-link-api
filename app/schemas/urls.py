from datetime import datetime
from sqlmodel import SQLModel

class Urls_response(SQLModel):
    id: int
    original_url: str
    short_url: str
    user_id: int
    created_at: datetime

class Urls_base(SQLModel):
    original_url: str