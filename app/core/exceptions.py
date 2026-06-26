class AppException(Exception):
    def __init__(self, message: str, code: int = 400, errors=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors

class ForbiddenError(AppException):
    def __init__(self, message: str, code: int = 403, errors=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors

# Auth exceptions
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

# Role exceptions
class RoleNotFoundError(AppException):
    def __init__(self, message: str = "Role not found", code: int = 404, errors=None):
        super().__init__(message, code, errors)

class RoleAlreadyExistsError(AppException):
    def __init__(self, message: str = "Role already exists", code: int = 400, errors=None):
        super().__init__(message, code, errors)

class SystemRoleDeleteError(AppException):
    def __init__(self, message: str = "Cannot delete system roles", code: int = 400, errors=None):
        super().__init__(message, code, errors)

class RoleNotAssignedError(AppException):
    def __init__(self, message: str = "User has no role assigned.", code: int = 403, errors=None):
        super().__init__(message, code, errors)

class PermissionDeniedError(AppException):
    def __init__(self, message: str = "Missing required permission", code: int = 403, errors=None):
        super().__init__(message, code, errors)
