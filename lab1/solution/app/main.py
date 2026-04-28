"""FastAPI iris classifier service.

Loads the trained model at startup and exposes:
  GET  /health        — liveness check
  POST /predict       — predict iris species from features
  GET  /predictions   — list recent predictions (read from Postgres)
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import joblib
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine, func
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# --- Configuration -----------------------------------------------------------

MODEL_PATH = Path(os.getenv("MODEL_PATH", "/app/model.joblib"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./predictions.db")

# --- Database ----------------------------------------------------------------

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    sepal_length = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    predicted_species = Column(String(32), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Model loading -----------------------------------------------------------

MODEL_BUNDLE: dict | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODEL_BUNDLE
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Did you run train.py?")
    MODEL_BUNDLE = joblib.load(MODEL_PATH)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Iris Classifier", version="1.0.0", lifespan=lifespan)


# --- Schemas -----------------------------------------------------------------

class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., ge=0, le=10, examples=[5.1])
    sepal_width: float = Field(..., ge=0, le=10, examples=[3.5])
    petal_length: float = Field(..., ge=0, le=10, examples=[1.4])
    petal_width: float = Field(..., ge=0, le=10, examples=[0.2])


class PredictionResponse(BaseModel):
    species: str
    probabilities: dict[str, float]


class PredictionLog(BaseModel):
    id: int
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    predicted_species: str

    class Config:
        from_attributes = True


# --- Routes ------------------------------------------------------------------

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(
    features: IrisFeatures,
    db: Annotated[Session, Depends(get_db)],
) -> PredictionResponse:
    if MODEL_BUNDLE is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    model = MODEL_BUNDLE["model"]
    target_names = MODEL_BUNDLE["target_names"]

    X = [[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]]

    probs = model.predict_proba(X)[0]
    pred_idx = int(probs.argmax())
    species = target_names[pred_idx]

    db.add(Prediction(
        sepal_length=features.sepal_length,
        sepal_width=features.sepal_width,
        petal_length=features.petal_length,
        petal_width=features.petal_width,
        predicted_species=species,
    ))
    db.commit()

    return PredictionResponse(
        species=species,
        probabilities={name: float(p) for name, p in zip(target_names, probs)},
    )


@app.get("/predictions", response_model=list[PredictionLog])
def list_predictions(
    db: Annotated[Session, Depends(get_db)],
    limit: int = 20,
) -> list[Prediction]:
    return (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .limit(limit)
        .all()
    )
