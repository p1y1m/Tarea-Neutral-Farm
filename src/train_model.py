"""
Train a simple ML model to predict Soil Organic Matter (OM) from proxies.
"""
from __future__ import annotations
import json
import joblib
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "organic_matter_dataset.csv"
ART = BASE / "model" / "artifacts"
ART.mkdir(parents=True, exist_ok=True)

FEATURES = ["pH", "EC", "Total Nitrogen", "Moisture"]
TARGET = "Organic Matter"

def main(seed: int = 42, test_size: float = 0.2) -> None:
    df = pd.read_csv(DATA)
    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )

    pre = ColumnTransformer(
        transformers=[("num", StandardScaler(), FEATURES)],
        remainder="drop"
    )
    model = Pipeline(steps=[("pre", pre), ("lr", LinearRegression())])
    model.fit(X_train, y_train)

    pred = model.predict(X_val)
    metrics = {
        "mae": float(mean_absolute_error(y_val, pred)),
        "rmse": float(mean_squared_error(y_val, pred, squared=False)),
        "r2": float(r2_score(y_val, pred)),
        "n_train": int(len(X_train)),
        "n_val": int(len(X_val))
    }
    (ART / "metrics.json").write_text(json.dumps(metrics, indent=2))
    joblib.dump(model, ART / "model.joblib")
    print("Saved:", ART / "model.joblib")
    print("Metrics:", json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
