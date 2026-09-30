from fastapi import HTTPException, Request
from .auth import get_user_id_from_token
from .database import get_user_by_id

COOKIE_NAME = "pocketsmart_token"

def current_user_optional(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    user_id = get_user_id_from_token(token)
    return get_user_by_id(user_id) if user_id else None

def current_user(request: Request):
    user = current_user_optional(request)
    if user is None:
        raise HTTPException(status_code=401, detail="Login required")
    return user
