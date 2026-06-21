from fastapi import FastAPI , HTTPException
from apps.routers.user_router import  router as user_router
app=FastAPI()

app.include_router(user_router)