from fastapi import FastAPI, HTTPException

from api.predictor import DamagePredictor
from api.schemas import PredictionRequest, PredictionResponse

app = FastAPI(
    title="Damage Mode Prediction API",
    version="1.0.0",
    description="Predict composite damage mode using Acoustic Emission features."
)

predictor = DamagePredictor()


@app.get("/")
def root():
    return {
        "message": "Damage Mode Prediction API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/features")
def features():
    return {
        "required_features": predictor.required_features()
    }


@app.post("/predict", response_model = PredictionResponse)
def predict(request: PredictionRequest):

    try:
        return predictor.predict(request.features)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
