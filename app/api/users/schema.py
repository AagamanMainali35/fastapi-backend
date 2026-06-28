from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreateModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Optional[str]
    password: Optional[str]
    email: EmailStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
        Validate the password against the given sets of rule.

        The password must:
        - Be between 8 and 12 characters long.
        - Contain at least one uppercase letter.
        - Contain at least one lowercase letter.
        - Contain at least one digit.
        - Contain at least one special character.

        Args:
            value: The password provided by the user.

        Returns:
            The validated password if it satisfies all requirements.

        Raises:
            ValueError: If the password does not meet one or more validation rules.
        """
        # NOTE : uncomment for the password policy

        # if len(value) < 8 or len(value) > 12:
        #     raise ValueError("Password must be between 8 and 12 characters.")

        # if not any(c.islower() for c in value):
        #     raise ValueError("Password must contain at least one lowercase letter.")

        # if not any(c.isupper() for c in value):
        #     raise ValueError("Password must contain at least one uppercase letter.")

        # if not any(c.isdigit() for c in value):
        #     raise ValueError("Password must contain at least one number.")

        # if not any(not c.isalnum() for c in value):
        #     raise ValueError("Password must contain at least one special character.")

        return value


class UserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    username: str = Field(validation_alias="user_name")
    email: EmailStr


class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
