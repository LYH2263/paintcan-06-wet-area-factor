from fastapi import APIRouter, HTTPException
from app.schemas.estimate import EstimateRequest
from app.services.paint_service import PaintService, WetFactorError
router = APIRouter()
@router.post("/estimate")
def post_estimate(body: EstimateRequest):
    with PaintService() as s:
        try:
            r = s.estimate(body.room_id, body.persist, body.coats, body.coverage)
        except WetFactorError as e:
            # 系数 <=0 整单拒绝（且服务层在写记录前抛出，不落库）
            raise HTTPException(400, str(e))
        if not r: raise HTTPException(404)
        return r
