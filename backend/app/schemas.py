from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AnalyzeRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    source_type: Literal["sms", "email", "chat"] = "chat"


class Technique(BaseModel):
    name: str
    severity: Literal["low", "medium", "high"]
    explanation: str
    evidence: list[str]


class ScanResponse(BaseModel):
    id: str
    message: str
    source_type: str
    trust_score: int
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    detected_techniques: list[Technique]
    explanation: str
    recommendation: str
    nlp_mode: str
    created_at: datetime
