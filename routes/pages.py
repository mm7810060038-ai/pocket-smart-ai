import json
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..config import TEMPLATE_DIR
from ..dependencies import current_user_optional, current_user
from ..database import list_recommendations, get_recommendation

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def render(request: Request, name: str, **context):
    # Explicit keyword arguments are compatible with current Starlette versions.
    context["request"] = request
    context["user"] = current_user_optional(request)
    return templates.TemplateResponse(request=request, name=name, context=context)

@router.get("/")
async def index(request: Request):
    return render(request, "index.html")

@router.get("/testimonials")
async def testimonials(request: Request):
    return render(request, "testimonials.html")

@router.get("/dashboard")
async def dashboard(request: Request):
    user = current_user(request)
    rows = list_recommendations(user["id"], 5)
    return render(request, "dashboard.html", recommendations=rows)

@router.get("/home-planner")
async def home_planner(request: Request):
    if not current_user_optional(request):
        return RedirectResponse("/login", status_code=303)
    return render(request, "home_planner.html")

@router.get("/party-planner")
async def party_planner(request: Request):
    if not current_user_optional(request):
        return RedirectResponse("/login", status_code=303)
    return render(request, "party_planner.html")

@router.get("/jewelry-planner")
async def jewelry_planner(request: Request):
    if not current_user_optional(request):
        return RedirectResponse("/login", status_code=303)
    return render(request, "jewelry_planner.html")

@router.get("/history")
async def history(request: Request):
    user = current_user_optional(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return render(request, "history.html", recommendations=list_recommendations(user["id"]))

@router.get("/recommendation/{record_id}")
async def recommendation(request: Request, record_id: int):
    user = current_user_optional(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    row = get_recommendation(user["id"], record_id)
    if not row:
        return RedirectResponse("/history", status_code=303)
    result = json.loads(row["result_json"])
    return render(request, "recommendation.html", record=row, result=result)
