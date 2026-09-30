import json
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from ..database import save_recommendation
from ..dependencies import current_user
from ..services import gemini_service
from ..config import MAX_UPLOAD_MB, UPLOAD_DIR

router = APIRouter()


def _save(user, category, payload, result):
    record_id = save_recommendation(user["id"], category, json.dumps(payload), json.dumps(result))
    return {"id": record_id, "category": category, "result": result}

@router.post("/generate-home")
async def generate_home(budget: float = Form(...), room: str = Form(...), style: str = Form("Modern"), items: str = Form("Lights, fan, table"), user=Depends(current_user)):
    if budget <= 0:
        return JSONResponse({"detail": "Budget must be greater than zero."}, status_code=422)
    payload = {"budget": budget, "room": room, "style": style, "items": items}
    return _save(user, "home", payload, gemini_service.home(payload))

@router.post("/generate-party")
async def generate_party(budget: float = Form(...), guests: int = Form(...), event_type: str = Form(...), venue: str = Form("Chennai"), user=Depends(current_user)):
    if budget <= 0 or guests <= 0:
        return JSONResponse({"detail": "Budget and guests must be greater than zero."}, status_code=422)
    payload = {"budget": budget, "guests": guests, "event_type": event_type, "venue": venue}
    return _save(user, "party", payload, gemini_service.party(payload))

@router.post("/generate-jewelry")
async def generate_jewelry(budget: float = Form(...), occasion: str = Form(...), style: str = Form("Elegant"), outfit: str = Form(""), outfit_image: UploadFile | None = File(None), user=Depends(current_user)):
    if budget <= 0:
        return JSONResponse({"detail": "Budget must be greater than zero."}, status_code=422)
    image_name = None
    if outfit_image and outfit_image.filename:
        allowed = {".jpg", ".jpeg", ".png", ".webp"}
        suffix = Path(outfit_image.filename).suffix.lower()
        if suffix not in allowed:
            return JSONResponse({"detail": "Only JPG, JPEG, PNG and WEBP images are allowed."}, status_code=400)
        data = await outfit_image.read()
        if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
            return JSONResponse({"detail": f"Image must be smaller than {MAX_UPLOAD_MB} MB."}, status_code=400)
        image_name = f"{uuid4().hex}{suffix}"
        (UPLOAD_DIR / image_name).write_bytes(data)
    payload = {"budget": budget, "occasion": occasion, "style": style, "outfit": outfit, "outfit_image": image_name}
    return _save(user, "jewelry", payload, gemini_service.jewelry(payload))
