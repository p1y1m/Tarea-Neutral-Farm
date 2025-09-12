from __future__ import annotations
from pydantic import BaseModel, Field

class IngestPayload(BaseModel):
    pH: float = Field(..., ge=0, le=14)
    EC: float = Field(..., ge=0)
    Total_Nitrogen: float = Field(..., ge=0)
    Moisture: float = Field(..., ge=0, le=100)
    Organic_Matter: float | None = Field(None, ge=0)

class PredictPayload(BaseModel):
    pH: float = Field(..., ge=0, le=14)
    EC: float = Field(..., ge=0)
    Total_Nitrogen: float = Field(..., ge=0)
    Moisture: float = Field(..., ge=0, le=100)

class PredictResponse(BaseModel):
    predicted_organic_matter: float
