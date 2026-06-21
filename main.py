from apps.routers.user_router import router as user_router
from fastapi import FastAPI, HTTPException

app = FastAPI()

app.include_router(user_router)
