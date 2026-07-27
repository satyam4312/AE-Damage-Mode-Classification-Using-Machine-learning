from typing import Dict

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """
    Input features for one AE hit.
    """

    features: Dict[str, float] = Field(
        ...,
        json_schema_extra={
            "example": {
                "Amp": 75.4,
                "RiseT": 51.0,
                "Dur": 185.2,
                "Eny": 1245.8,
                "Counts": 42,
                "RMS": 2.3,
                "SS": 480
            }
        }
    )


class PredictionResponse(BaseModel):
    damage_mode: str
    confidence: float | None
    probabilities: Dict[str, float]

