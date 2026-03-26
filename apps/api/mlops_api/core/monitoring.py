from dataclasses import dataclass
from threading import Lock


@dataclass
class Counters:
    total_requests: int = 0
    total_predictions: int = 0


class MonitoringStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._counters = Counters()

    def increment_requests(self) -> int:
        with self._lock:
            self._counters.total_requests += 1
            return self._counters.total_requests

    def increment_predictions(self) -> int:
        with self._lock:
            self._counters.total_predictions += 1
            return self._counters.total_predictions

    def snapshot(self) -> Counters:
        with self._lock:
            return Counters(
                total_requests=self._counters.total_requests,
                total_predictions=self._counters.total_predictions,
            )
