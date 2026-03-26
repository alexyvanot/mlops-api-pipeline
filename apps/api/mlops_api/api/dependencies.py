from fastapi import Request

from mlops_api.core.monitoring import MonitoringStore
from mlops_api.services.predictor import PredictorService


def get_predictor(request: Request) -> PredictorService:
    return request.app.state.predictor


def get_monitoring(request: Request) -> MonitoringStore:
    return request.app.state.monitoring
