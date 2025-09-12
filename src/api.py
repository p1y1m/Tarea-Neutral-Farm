
from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from .models import SoilRecord
from .schema import IngestPayload, PredictPayload, PredictResponse
from .utils import get_model

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Neutral Farming OM API", version="0.1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/data_ingestion')
def data_ingestion(payload: IngestPayload, db: Session = Depends(get_db)):
    record = SoilRecord(
        pH=payload.pH,
        EC=payload.EC,
        total_nitrogen=payload.Total_Nitrogen,
        moisture=payload.Moisture,
        organic_matter=payload.Organic_Matter,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {'id': record.id}

@app.post('/predict', response_model=PredictResponse)
def predict(payload: PredictPayload):
    import pandas as pd
    model = get_model()
    # construir DataFrame con los mismos nombres de columnas usados al entrenar
    X = pd.DataFrame([{
        'pH': payload.pH,
        'EC': payload.EC,
        'Total Nitrogen': payload.Total_Nitrogen,  # OJO: espacio como en el CSV
        'Moisture': payload.Moisture
    }])
    try:
        pred = float(model.predict(X)[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Prediction failed: {e}')
    return PredictResponse(predicted_organic_matter=round(pred, 4))
