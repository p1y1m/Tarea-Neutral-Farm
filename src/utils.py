from __future__ import annotations
from pathlib import Path
import joblib

ART = Path(__file__).resolve().parents[1] / "model" / "artifacts"
MODEL_PATH = ART / "model.joblib"

_model_cache = None

def get_model():
    global _model_cache
    if _model_cache is None:
        _model_cache = joblib.load(MODEL_PATH)
    return _model_cache
