# Auth API router
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.schemas import LoginRequest, RegisterRequest
from app.core.db import get_db
from app.domains.auth.services import Authservice

router = APIRouter(prefix="/auth", tags=["auth"])


@cbv(router)
class UserView:
    session: AsyncSession = Depends(get_db)

    @router.post("/register")
    async def register(
        self,
        user: RegisterRequest,
    ):
        result = Authservice.register_user(self.session, user.email, user.username, user.password)
        return await result
