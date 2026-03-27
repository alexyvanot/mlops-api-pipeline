import logging

from fastapi import APIRouter, Depends

from mlops_api.api.dependencies import get_monitoring, get_predictor
from mlops_api.core.monitoring import MonitoringStore
from mlops_api.core.settings import ApiSettings
from mlops_api.core.version import get_version_info
from mlops_api.schemas.prediction import (
    HealthResponse,
    MetricsResponse,
    PredictionRequest,
    PredictionResponse,
    VersionResponse,
)
from mlops_api.services.predictor import PredictorService

router = APIRouter()
logger = logging.getLogger("mlops_api")
settings = ApiSettings()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    info = get_version_info(settings.app_version)
    return VersionResponse(
        app_version=info.app_version,
        git_commit=info.git_commit,
        git_branch=info.git_branch,
    )


@router.get("/metrics", response_model=MetricsResponse)
def metrics(monitoring: MonitoringStore = Depends(get_monitoring)) -> MetricsResponse:
    counters = monitoring.snapshot()
    return MetricsResponse(
        total_requests=counters.total_requests,
        total_predictions=counters.total_predictions,
    )


@router.post("/predict", response_model=PredictionResponse)
def predict(
    payload: PredictionRequest,
    predictor: PredictorService = Depends(get_predictor),
    monitoring: MonitoringStore = Depends(get_monitoring),
) -> PredictionResponse:
    features = [
        payload.sepal_length,
        payload.sepal_width,
        payload.petal_length,
        payload.petal_width,
    ]
    result = predictor.predict(features)
    prediction_count = monitoring.increment_predictions()

    logger.info(
        "prediction_request features=%s prediction=%s class_name=%s",
        features,
        result.prediction,
        result.class_name,
    )

    return PredictionResponse(
        prediction=result.prediction,
        class_name=result.class_name,
        prediction_count=prediction_count,
    )
