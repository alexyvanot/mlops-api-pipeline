from dataclasses import dataclass

import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from .config import Settings
from .dataset import FEATURE_NAMES, load_training_data
from .registry import save_model


@dataclass(frozen=True)
class TrainingResult:
    accuracy: float
    model_path: str


def train_and_log(settings: Settings) -> TrainingResult:
    x, y = load_training_data()

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=settings.random_state,
        stratify=y,
    )

    model = RandomForestClassifier(n_estimators=200, random_state=settings.random_state)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    with mlflow.start_run(run_name="train-random-forest"):
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("random_state", settings.random_state)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_dict({"features": FEATURE_NAMES}, "feature_schema.json")

    save_model(model, settings.model_path)
    return TrainingResult(accuracy=accuracy, model_path=str(settings.model_path))
