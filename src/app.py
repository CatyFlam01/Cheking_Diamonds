from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.data_processing import add_features
from src.model_training import FEATURE_COLUMNS, METRICS_PATH, MODEL_PATH, load_model
from src.monitoring import get_infrastructure_metrics


app = FastAPI(title="Diamonds Price Prediction API", version="1.0.0")
model: Any | None = load_model()


class DiamondFeatures(BaseModel):
    carat: float = Field(gt=0)
    cut: str
    color: str
    clarity: str
    depth: float = Field(gt=0)
    table: float = Field(gt=0)
    x: float = Field(gt=0)
    y: float = Field(gt=0)
    z: float = Field(gt=0)


def _get_model() -> Any:
    global model
    if model is None:
        model = load_model()
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not trained yet. Run python -m src.model_training.")
    return model


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Diamonds price prediction API", "docs": "/docs"}


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "model_loaded": model is not None or MODEL_PATH.exists(),
        "infrastructure": get_infrastructure_metrics(),
    }


@app.post("/predict")
def predict(features: DiamondFeatures) -> dict[str, float]:
    active_model = _get_model()
    payload = features.model_dump() if hasattr(features, "model_dump") else features.dict()
    frame = pd.DataFrame([payload])
    frame = add_features(frame)
    prediction = float(active_model.predict(frame[FEATURE_COLUMNS])[0])
    return {"predicted_price": round(prediction, 2)}


@app.get("/model/info")
def model_info() -> dict[str, Any]:
    metrics: dict[str, Any] | None = None
    if Path(METRICS_PATH).exists():
        metrics = json.loads(Path(METRICS_PATH).read_text(encoding="utf-8"))
    return {
        "model_path": str(MODEL_PATH),
        "model_exists": MODEL_PATH.exists(),
        "metrics": metrics,
        "features": FEATURE_COLUMNS,
    }
