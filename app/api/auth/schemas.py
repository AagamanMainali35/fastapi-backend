# Pydantic schemas for Auth
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class LoginRequest(UserBase):
    password: str


class RegisterRequest(UserBase):
    username: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    email: str
    username: str = Field(validation_alias="user_name")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class MessageResponse(BaseModel):
    message: str
