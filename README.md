# Neutral Farming – Soil Organic Matter (OM) Predictor

End-to-end proof of concept: train a simple ML model to predict **Organic Matter** (OM) from **pH, EC, Total Nitrogen, Moisture**, and serve it via a FastAPI backend with data ingestion to SQLite.

## 🧠 Model (Part 1)

- **Choice**: `LinearRegression` in a `Pipeline(StandardScaler -> LinearRegression)`.
  - **Why**: Tiny dataset, low variance, interpretable coefficients, fast training/serving, strong baseline.
- **Metrics**: Saved to `model/artifacts/metrics.json` after training. Example from this run:
```json
{
  "mae": 0.13336367648681446,
  "rmse": 0.14653228960860773,
  "r2": 0.9561801798001206,
  "n_train": 8,
  "n_val": 2
}
```
- **Artifacts**: Trained model in `model/artifacts/model.joblib`.

### Train
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python src/train_model.py
cat model/artifacts/metrics.json
```

## 🗄️ Backend (Part 2)

- **DB**: SQLite (`om.db`) via SQLAlchemy.
- **Endpoints**:
  - `POST /data_ingestion` → store new record {pH, EC, Total_Nitrogen, Moisture, Organic_Matter?}
  - `POST /predict` → predict OM from the 4 proxies.

### Run API
```bash
uvicorn src.api:app --reload
```

### Example requests
```bash
# Ingest labeled sample
curl -X POST http://127.0.0.1:8000/data_ingestion   -H "Content-Type: application/json"   -d '{"pH": 6.8, "EC": 0.25, "Total_Nitrogen": 0.12, "Moisture": 28, "Organic_Matter": 3.8}'

# Predict
curl -X POST http://127.0.0.1:8000/predict   -H "Content-Type: application/json"   -d '{"pH": 7.0, "EC": 0.3, "Total_Nitrogen": 0.15, "Moisture": 30}'
```

## 🧱 Project Layout
```
neutral-farming-om/
  data/organic_matter_dataset.csv
  model/artifacts/          # model.joblib + metrics.json
  src/
    api.py                  # FastAPI app with /data_ingestion and /predict
    train_model.py          # training script
    db.py, models.py        # SQLite via SQLAlchemy
    schema.py               # Pydantic request/response models
    utils.py                # model loader
  requirements.txt
  README.md
```

## 🧪 Notes
- Schema validation uses **Pydantic** to keep inputs clean and ranges realistic.
- For production: swap SQLite → PostgreSQL by changing `DATABASE_URL` in `src/db.py`.

## 🗣️ How to explain in interview (TL;DR)
1. **Problem framing**: predict OM from cheap proxies (pH, EC, N, Moisture) to avoid costly lab work.
2. **Baseline-first**: chose Linear Regression + scaling: transparent, fast, good bias-variance tradeoff on tiny data.
3. **Validation**: train/validation split, reported MAE/RMSE/R²; stored metrics + model artifact.
4. **Serving**: FastAPI with two routes: data ingestion (DB write) and prediction (load cached model → respond JSON).
5. **Extensibility**: retraining hook (run `train_model.py`), easy DB swap to Postgres, containerizable.
