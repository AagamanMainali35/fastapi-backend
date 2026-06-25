from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.schemas import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    ResendVerificationRequest,
    TokenResponse,
    UserResponse,
    VerifyEmailRequest,
)
from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import AppException
from app.domains.auth.dependencies import get_current_active_user
from app.domains.auth.models import User
from app.domains.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201, name="register")
async def register(
    user: RegisterRequest,
    session: AsyncSession = Depends(get_db),  # noqa: B008
):
    return await AuthService.register_user(session, user.email, user.username, user.password)


@router.post("/login", response_model=TokenResponse, name="login")
async def login(user: LoginRequest, session: AsyncSession = Depends(get_db)):  # noqa: B008
    return await AuthService.login(session, user.email, user.password)


@router.post("/verify-email", response_model=MessageResponse, name="verify_email")
async def verify_email(request: VerifyEmailRequest, session: AsyncSession = Depends(get_db)):  # noqa: B008
    return await AuthService.verify_email(session, request.email, request.code)


@router.post("/resend-verification", response_model=MessageResponse, name="resend_verification")
async def resend_verification(request: ResendVerificationRequest, session: AsyncSession = Depends(get_db)):  # noqa: B008
    return await AuthService.resend_verification_code(session, request.email)


@router.get("/me", response_model=UserResponse, name="me")
async def me(current_user: User = Depends(get_current_active_user)):  # noqa: B008
    return current_user


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = str(request.url_for("google_callback"))

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "select_account",
    }

    google_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)

    return RedirectResponse(google_url)


@router.get("/google/callback", response_model=TokenResponse, name="google_callback")
async def google_callback(request: Request, session: AsyncSession = Depends(get_db)):  # noqa: B008
    code = request.query_params.get("code")

    if not code:
        raise AppException(message="No authorization code received", code=400)

    redirect_uri = str(request.url_for("google_callback"))

    google_user = await AuthService.exchange_google_code(code, redirect_uri)

    return await AuthService.google_login_or_register(
        session,
        email=google_user["email"],
        name=google_user["name"],
        google_id=google_user["google_id"],
    )
