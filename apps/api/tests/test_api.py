from fastapi.testclient import TestClient

from mlops_api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version() -> None:
    response = client.get("/version")
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {"app_version", "git_commit", "git_branch"}
    assert isinstance(body["app_version"], str)
    assert isinstance(body["git_commit"], str)
    assert isinstance(body["git_branch"], str)


def test_predict_and_metrics() -> None:
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    prediction_response = client.post("/predict", json=payload)
    assert prediction_response.status_code == 200

    body = prediction_response.json()
    assert set(body.keys()) == {"prediction", "class_name", "prediction_count"}
    assert body["class_name"] in {"setosa", "versicolor", "virginica"}

    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    metrics = metrics_response.json()
    assert metrics["total_requests"] >= 3
    assert metrics["total_predictions"] >= 1
