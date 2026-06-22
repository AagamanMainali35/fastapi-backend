# Pydantic schemas for Auth
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class LoginRequest(UserBase):
    password: str


class RegisterRequest(UserBase):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True
