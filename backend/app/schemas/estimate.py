from pydantic import BaseModel
class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    persist: bool = True
class RoomWetRequest(BaseModel):
    wet: bool
class SettingRequest(BaseModel):
    key: str
    value: str
