from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.core.base_execption import AppException
from app.core.config import settings
from app.core.db import get_db
from app.domains.auth.services import Authservice

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", name="register")
async def register(
    user: RegisterRequest,
    session: AsyncSession = Depends(get_db),  # noqa: B008
):
    return await Authservice.register_user(session, user.email, user.username, user.password)


@router.post("/login", name="login")
async def login(user: LoginRequest, session: AsyncSession = Depends(get_db)):  # noqa: B008
    return await Authservice.login(session, user.email, user.password)


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


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, session: AsyncSession = Depends(get_db)):  # noqa: B008

    code = request.query_params.get("code")

    if not code:
        return {"error": "No authorization code received"}

    redirect_uri = str(request.url_for("google_callback"))

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
        )

    if response.status_code != 200:
        raise AppException(message="Failed to exchange authorization code with Google", code=400, errors={"detail": response.text})

    token_data = response.json()

    if "id_token" not in token_data:
        raise AppException(message="No ID token found in Google response", code=400, errors=token_data)

    google_token = token_data["id_token"]

    try:
        google_user = id_token.verify_oauth2_token(google_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=10)
    except ValueError as e:
        raise AppException(message=f"Invalid Google ID token: {str(e)}", code=400)

    email = google_user["email"]
    google_id = google_user["sub"]
    name = google_user.get("name")

    # authenticate or register the user
    return await Authservice.google_login_or_register(session, email, name, google_id)


@router.post("/ping")
async def ping():
    print("🔥 PING HIT")
    return {"ok": True}
