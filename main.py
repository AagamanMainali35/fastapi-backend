from fastapi import FastAPI

from app.api.auth.router import router as user_router
from app.core.base_execption import AppException

app = FastAPI()
from fastapi import Request
from fastapi.responses import JSONResponse


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


app.include_router(user_router)
