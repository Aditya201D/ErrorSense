from pydantic import BaseModel


# ==========================
# Request Model
# ==========================

class UserInput(BaseModel):
    request: str = ""
    response: str = ""


# ==========================
# Response Models
# ==========================

class AlternativePrediction(BaseModel):
    category: str
    confidence: float


class PredictionResponse(BaseModel):
    category: str
    confidence: float
    resolution: str
    alternatives: list[AlternativePrediction]
    severity: str
    module: str
    next_step: str
    documentation: str


class ErrorResponse(BaseModel):
    error: str


class StatusResponse(BaseModel):
    status: str