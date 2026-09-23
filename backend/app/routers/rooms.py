from fastapi import APIRouter, HTTPException
from app.schemas.rooms import DampRequest
from app.services.paint_service import PaintService
router = APIRouter()
@router.get("/rooms")
def list_rooms():
    with PaintService() as s: return {"items": s.list_rooms()}
@router.get("/rooms/{room_id}")
def room_detail(room_id: int):
    with PaintService() as s:
        d = s.room_detail(room_id)
        if not d: raise HTTPException(404)
        return d
@router.put("/rooms/{room_id}/damp")
def set_damp(room_id: int, body: DampRequest):
    with PaintService() as s:
        d = s.set_damp(room_id, body.damp)
        if not d: raise HTTPException(404)
        return d
