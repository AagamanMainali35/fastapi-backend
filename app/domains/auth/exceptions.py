from app.core.base_execption import AppException


class InvalidCredentialsError(AppException):
    def __init__(self, message: str = "Invalid credentials", code: int = 401, errors=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors


class UserAlreadyExistsError(AppException):
    def __init__(
        self,
        message: str = "User already exists",
        code: int = 400,
        errors=None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors
