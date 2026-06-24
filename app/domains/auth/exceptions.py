from app.core.exceptions import AppException


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


class EmailVerificationError(AppException):
    def __init__(self, message: str = "Invalid or expired verification code", code: int = 400, errors=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors


class UserNotVerifiedError(AppException):
    def __init__(self, message: str = "User email not verified", code: int = 403, errors=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors
