from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Lab 2 MLOps Model API",
    description="Containerised FastAPI service with Pydantic validation",
    version="1.0.0"
)

class PredictionInput(BaseModel):
    feature1: float = Field(..., description="First feature value")
    feature2: float = Field(..., description="Second feature value")

class PredictionResponse(BaseModel):
    prediction: int
    probability: float

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionInput):
    try:
        val = data.feature1 + data.feature2
        pred_class = 1 if val > 10 else 0
        prob = 0.85 if pred_class == 1 else 0.15
        
        return {
            "prediction": pred_class,
            "probability": prob
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))