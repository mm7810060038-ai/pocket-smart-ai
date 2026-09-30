from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
from ..auth import hash_password, verify_password, create_access_token
from ..database import create_user, get_user_by_email, get_user_by_id
from ..dependencies import COOKIE_NAME, current_user_optional
from fastapi.templating import Jinja2Templates
from ..config import TEMPLATE_DIR

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

router = APIRouter()


def page(request: Request, name: str, **context):
    context["request"] = request
    context["user"] = current_user_optional(request)
    return templates.TemplateResponse(request=request, name=name, context=context)

@router.get("/register")
async def register_page(request: Request):
    if current_user_optional(request):
        return RedirectResponse("/dashboard", status_code=303)
    return page(request, "register.html")

@router.post("/register")
async def register(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    name, email = name.strip(), email.strip().lower()
    if len(name) < 2 or len(password) < 6 or "@" not in email:
        return page(request, "register.html", error="Enter a valid name, email and password (minimum 6 characters).")
    if get_user_by_email(email):
        return page(request, "register.html", error="An account with this email already exists.")
    user_id = create_user(name, email, hash_password(password))
    token = create_access_token(user_id)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(COOKIE_NAME, token, httponly=True, samesite="lax", max_age=86400)
    return response

@router.get("/login")
async def login_page(request: Request):
    if current_user_optional(request):
        return RedirectResponse("/dashboard", status_code=303)
    return page(request, "login.html")

@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email.strip().lower())
    if not user or not verify_password(password, user["password_hash"]):
        return page(request, "login.html", error="Invalid email or password.")
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(COOKIE_NAME, create_access_token(user["id"]), httponly=True, samesite="lax", max_age=86400)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(COOKIE_NAME)
    return response

@router.post("/token")
async def token(email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email.strip().lower())
    if not user or not verify_password(password, user["password_hash"]):
        return JSONResponse({"detail": "Invalid credentials"}, status_code=401)
    return {"access_token": create_access_token(user["id"]), "token_type": "bearer"}

@router.get("/session-info")
async def session_info(request: Request):
    user = current_user_optional(request)
    return {"logged_in": bool(user), "user_id": user["id"] if user else None, "name": user["name"] if user else None}

@router.get("/session-data")
async def session_data(request: Request):
    user = current_user_optional(request)
    if not user:
        return JSONResponse({"detail": "Login required"}, status_code=401)
    return {"user": {"id": user["id"], "name": user["name"], "email": user["email"]}}
