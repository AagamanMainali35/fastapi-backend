from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.auth.router import router as auth_router
from app.api.roles.router import router as roles_router
from app.api.users.router import router as users_router
from app.core.exceptions import AppException

app = FastAPI(
    title="FastAPI App",
    version="0.1.0",
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "message": exc.message,
            "errors": exc.errors,
        },
    )


api_v1_prefix = "/api/v1"

app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(roles_router, prefix=api_v1_prefix)
app.include_router(users_router, prefix=api_v1_prefix)
