import logging
import time

from fastapi import FastAPI, Request

from mlops_api.api.routes import router
from mlops_api.core.logging import configure_logging
from mlops_api.core.monitoring import MonitoringStore
from mlops_api.core.settings import ApiSettings
from mlops_api.services.predictor import PredictorService

settings = ApiSettings()
configure_logging(settings.log_level)
logger = logging.getLogger("mlops_api")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.monitoring = MonitoringStore()
app.state.predictor = PredictorService()


@app.middleware("http")
async def track_requests(request: Request, call_next):
    started_at = time.perf_counter()
    request_count = request.app.state.monitoring.increment_requests()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started_at) * 1000
    logger.info(
        "request method=%s path=%s status=%s duration_ms=%.2f total_requests=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_count,
    )
    return response


app.include_router(router)
