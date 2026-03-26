from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    model_path: Path = Field(default=Path("artifacts/model.pkl"), alias="MODEL_PATH")
    mlflow_tracking_uri: str = Field(default="file:./mlruns", alias="MLFLOW_TRACKING_URI")
    mlflow_experiment_name: str = Field(default="mlops-api-pipeline", alias="MLFLOW_EXPERIMENT_NAME")
    random_state: int = Field(default=42, alias="RANDOM_STATE")
