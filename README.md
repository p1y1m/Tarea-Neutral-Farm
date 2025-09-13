**Neutral Farming – Soil organic matter (OM) predictor**

End to end proof of concept. Train a simple ML model to predict organic matter (OM) from pH, EC, total nitrogen, moisture, and serve it via a fastapi backend with data ingestion to sqlite.

**Model (Part 1)**

Choice: LinearRegression in a Pipeline(StandardScaler, LinearRegression).
Why: tiny dataset, low variance, interpretable coeficients, fast training/serving, strong baseline.
Metrics saved to model/artifacts/metrics.json after training. example from this run:

{
"mae": 0.1333636764868144,
"rmse": 0.14653228960860773,
"r2": 0.9561801798001206,
"n_train": 8,
"n_val": 2
}

Artifacts: trained model in model/artifacts/model.joblib

**Train**
python -m venv .venv && source .venv/bin/activate # windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/train_model.py
cat model/artifacts/metrics.json

**Backend (Part 2)**

DB: sqlite (om.db) with sqlalchemy
Endpoints:
POST /data_ingestion: store new record {pH, EC, Total_Nitrogen, Moisture, Organic_Matter?}
POST /predict: predict om from the 4 proxies

Run api
uvicorn src.api:app --reload

**Example requests**
curl -X POST http://127.0.0.1:8000/data_ingestion
 -H "Content-Type: application/json" -d '{"pH": 6.8, "EC": 0.25, "Total_Nitrogen": 0.12, "Moisture": 28, "Organic_Matter": 3.8}'

curl -X POST http://127.0.0.1:8000/predict
 -H "Content-Type: application/json" -d '{"pH": 7.0, "EC": 0.3, "Total_Nitrogen": 0.15, "Moisture": 30}'

**Project layout**

neutral-farming-om/
data/organic_matter_dataset.csv
model/artifacts/ - model.joblib + metrics.json
src/
api.py - fastapi app with /data_ingestion and /predict
train_model.py - training script
db.py, models.py - sqlite via sqlalchemy
schema.py - pydantic request/response models
utils.py - model loader
requirements.txt
readme.md

**Notes**

schema validation uses pydantic to keep inputs clean and ranges realistic.
for production swap sqlite to postgresql by changing DATABASE_URL in src/db.py
