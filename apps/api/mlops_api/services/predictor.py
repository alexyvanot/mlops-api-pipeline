from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.mlops_ml.config import Settings as MlSettings
from packages.mlops_ml.registry import load_model
from packages.mlops_ml.trainer import train_and_log


CLASS_MAPPING = {0: "setosa", 1: "versicolor", 2: "virginica"}


@dataclass
class PredictionResult:
    prediction: int
    class_name: str


class PredictorService:
    def __init__(self, model_path: Path | None = None) -> None:
        settings = MlSettings()
        self._model_path = model_path or settings.model_path
        self._model = self._load_or_train()

    def _load_or_train(self) -> Any:
        if self._model_path.exists():
            return load_model(self._model_path)

        settings = MlSettings(model_path=self._model_path)
        train_and_log(settings)
        return load_model(self._model_path)

    def predict(self, features: list[float]) -> PredictionResult:
        pred = int(self._model.predict([features])[0])
        return PredictionResult(prediction=pred, class_name=CLASS_MAPPING[pred])
