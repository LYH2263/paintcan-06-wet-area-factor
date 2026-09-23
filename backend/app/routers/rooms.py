from fastapi import APIRouter, HTTPException
from app.schemas.estimate import RoomWetRequest
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
@router.patch("/rooms/{room_id}/wet")
def set_room_wet(room_id: int, body: RoomWetRequest):
    with PaintService() as s:
        r = s.set_room_wet(room_id, body.wet)
        if r is None: raise HTTPException(404)
        return {"room": r}
