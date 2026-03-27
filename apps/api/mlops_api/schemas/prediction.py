from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    sepal_length: float = Field(..., ge=0)
    sepal_width: float = Field(..., ge=0)
    petal_length: float = Field(..., ge=0)
    petal_width: float = Field(..., ge=0)


class PredictionResponse(BaseModel):
    prediction: int
    class_name: str
    prediction_count: int


class HealthResponse(BaseModel):
    status: str


class MetricsResponse(BaseModel):
    total_requests: int
    total_predictions: int


class VersionResponse(BaseModel):
    app_version: str
    git_commit: str
    git_branch: str
