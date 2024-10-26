from typing import Optional
from api.v1.schemas.base_schema import BaseResponseModel


class AsciiTaskStartResponse(BaseResponseModel):
    task_id: Optional[str]
