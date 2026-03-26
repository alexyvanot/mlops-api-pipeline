from pathlib import Path
from typing import Any

import joblib


ModelType = Any


def save_model(model: ModelType, model_path: Path) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)


def load_model(model_path: Path) -> ModelType:
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)
