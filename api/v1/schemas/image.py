from pydantic import BaseModel
from api.v1.schemas.base_schema import BaseResponseModel


class AsciiResultResponse(BaseResponseModel):
    result: str
