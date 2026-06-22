from fastapi import FastAPI, HTTPException

from app.api.auth.router import router as user_router

app = FastAPI()

app.include_router(user_router)
