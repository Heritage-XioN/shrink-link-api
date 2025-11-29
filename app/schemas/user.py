from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel

# schema for getting a user
class UserBase(SQLModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

# schema for the response for the of the register user route
class UserResponse(SQLModel):
    status: str

class Get_current_user(UserBase):
    pass
