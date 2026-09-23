from pydantic import BaseModel
class DampRequest(BaseModel):
    damp: bool
