from pydantic import EmailStr
from sqlmodel import SQLModel



# schema for login response
class AuthResponse(SQLModel):
    access_token: str
    token_type: str

# schema for incoming login details
class LoginAuth(SQLModel):
    email: EmailStr
    password: str

# schema for email verification response
class Email_verif_res(SQLModel):
    message: str