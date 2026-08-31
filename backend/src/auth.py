from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from . import config
from .db import SessionLocal, User

oauth = OAuth()
oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": config.GOOGLE_SCOPES},
)

router = APIRouter()


@router.get("/backend/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(
        request, config.REDIRECT_URI, access_type="offline", prompt="consent"
    )


@router.get("/backend/auth")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]

    with SessionLocal() as db:
        user = db.query(User).filter_by(google_sub=userinfo["sub"]).one_or_none()
        if user is None:
            user = User(google_sub=userinfo["sub"], email=userinfo["email"], refresh_token=token.get("refresh_token") or "")
            db.add(user)
        else:
            user.email = userinfo["email"]
            if token.get("refresh_token"):
                user.refresh_token = token["refresh_token"]
        db.commit()
        db.refresh(user)
        request.session["user_id"] = user.id

    return RedirectResponse(config.FRONTEND_URL)


@router.get("/backend/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(config.FRONTEND_URL)


@router.get("/backend/me")
async def me(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return {"logged_in": False}
    with SessionLocal() as db:
        user = db.get(User, user_id)
        if not user:
            return {"logged_in": False}
        return {
            "logged_in": True,
            "email": user.email,
            "calendar_url": f"{config.FRONTEND_URL}/backend/calendar/{user.calendar_token}.ics",
        }
