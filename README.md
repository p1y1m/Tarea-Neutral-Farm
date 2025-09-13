**Done by:** Pedro Yáñez Meléndez

**Project name:** Neutral Farming OM API

**Goal:** predict soil organic matter using proxy variables and expose a simple API for ingestion and prediction

---

**What is included:**  
- **Model:** Linear Regression with standard scaling  
- **Data:** `data/organic_matter_dataset.csv`  
- **Artifacts:** `model/artifacts/model.joblib` and `model/artifacts/metrics.json`  
- **API:** FastAPI with `/data_ingestion` and `/predict`  
- **Database:** SQLite with automatic table creation on app start  
- **Validation:** train and validation split with metrics (MAE, RMSE, R2)

---

**Folder structure:**  
- **data:** sample dataset  
- **model/artifacts:** trained model and metrics  
- **src:** source code  
  - **train_model.py:** trains and saves artifacts  
  - **utils.py:** loads and caches the trained model  
  - **db.py:** SQLAlchemy connection (SQLite by default)  
  - **models.py:** ORM table definition  
  - **schema.py:** request validation with Pydantic  
  - **api.py:** FastAPI endpoints and app startup  
- **requirements.txt:** dependencies

---

**Prerequisites:**  
- **Python:** 3.10 or 3.11  
- **Pip:** up to date  
- **Optional:** virtualenv

---

**Local setup:**  
1. **Create env:**  
   - Windows: `python -m venv .venv`  
   - Mac or Linux: `python3 -m venv .venv`  
2. **Activate env:**  
   - Windows: `.venv\Scripts\activate`  
   - Mac or Linux: `source .venv/bin/activate`  
3. **Install:** `pip install -r requirements.txt`

---

**Train the model:**  
- **Command:** `python src/train_model.py`  
- **Output:**  
  - `model/artifacts/model.joblib`  
  - `model/artifacts/metrics.json` (mae, rmse, r2, n_train, n_val)

---

**Database:**  
- **Engine:** SQLite file `om.db`  
- **Table creation:** automatic on API start with `create_all`  
- **Migrations:** not used in this version  
- **Switch to PostgreSQL:** edit `DATABASE_URL` in `src/db.py`

---

**Start the API:**  
- **Command:** `uvicorn src.api:app --reload`  
- **Local URL:** `http://127.0.0.1:8000`  
- **Docs:** `http://127.0.0.1:8000/docs`

---

**Test endpoints:**  
- **Data ingestion:**  
  ```
  POST /data_ingestion
  Content-Type: application/json

  {
    "pH": 6.9,
    "EC": 0.28,
    "Total_Nitrogen": 0.14,
    "Moisture": 29,
    "Organic_Matter": 4.1
  }
  ```
  **Response:** `{"id": 1}`

- **Prediction:**  
  ```
  POST /predict
  Content-Type: application/json

  {
    "pH": 6.7,
    "EC": 0.25,
    "Total_Nitrogen": 0.12,
    "Moisture": 28
  }
  ```
  **Response:** `{"predicted_organic_matter": 3.8}`  
  **Note:** field names match the training columns

---

**Run on Google Colab (optional):**  
- **Notebook flow:** mount Drive if you want persistence, install `requirements.txt`, run `src/train_model.py`, start Uvicorn  
- **Public testing:** Cloudflare Tunnel can expose the local URL for quick tests  
- **Benefit:** clean environment with step by step documentation inside the notebook

---

**Design decisions:**  
- **Simple model:** Linear Regression fits a tiny dataset, fast and interpretable  
- **Single pipeline:** scaler and model saved together to avoid data leakage and to simplify serving  
- **REST API:** clear JSON contract for easy integration  
- **Light DB:** SQLite for demo and tests with an easy path to PostgreSQL  
- **Assignment fit:** trained model, evaluation, stored artifact, ingestion endpoint, prediction endpoint, clear code layout, documentation, easy run

---

**How to read metrics:**  
- **File:** `model/artifacts/metrics.json`  
- **Goal:** low MAE and RMSE, high R2  
- **Note:** validation size is small, cross validation is recommended when more data is available

---

**Environment variables (optional):**  
- **DATABASE_URL:** switch database if needed  
- **Artifacts path:** keep `model/artifacts` for simplicity

---

**Troubleshooting:**  
- **Table not created:** start the API, creation is automatic  
- **Prediction error:** check JSON field names and numeric types  
- **No artifacts:** run `src/train_model.py` and check write permissions  
- **Colab persistence:** save artifacts inside mounted Drive

---

**Future work:**  
- **Cross validation and more data**  
- **Confidence intervals for metrics**  
- **Alembic for migrations**  
- **Docker and Compose**  
- **Auth and rate limiting**  
- **Structured logging and tracing**

