from fastapi import APIRouter
from app.schemas.estimate import SettingRequest
from app.services.paint_service import PaintService
router = APIRouter()
@router.get("/settings")
def settings():
    with PaintService() as s: return s.settings()
@router.put("/settings")
def put_settings(body: SettingRequest):
    with PaintService() as s:
        s.set_setting(body.key, body.value)
        return {body.key: body.value}
