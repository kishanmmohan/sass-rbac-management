from pydantic import BaseModel


class BaseResponse(BaseModel):
    message: str
    code: int
