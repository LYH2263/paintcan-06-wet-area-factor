from fastapi import APIRouter, HTTPException
from app.schemas.settings import SettingRequest
from app.services.paint_service import PaintService
router = APIRouter()
ALLOWED_KEYS = {"coverage", "coats", "damp_factor"}
@router.get("/settings")
def settings():
    with PaintService() as s: return s.settings()
@router.put("/settings/{key}")
def put_setting(key: str, body: SettingRequest):
    if key not in ALLOWED_KEYS: raise HTTPException(400, f"unknown setting: {key}")
    with PaintService() as s: return s.update_setting(key, body.value)
