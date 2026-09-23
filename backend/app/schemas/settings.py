from pydantic import BaseModel
class SettingRequest(BaseModel):
    value: str
