from typing import Optional

from pydantic import BaseModel
from api.v1.schemas.base_schema import BaseResponseModel


class RegisterRequest(BaseModel):
    username: str
    password: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseResponseModel):
    access_token: str


class AuthResponseData(BaseModel):
    id: str
    username: str


class AuthResponse(BaseResponseModel):
    access_token: str
    refresh_token: str
    data: AuthResponseData
