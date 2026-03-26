# mlops-api-pipeline

Python monorepo for a DevOps/MLOps mini-project with:
- MLOps pipeline (scikit-learn training + `.pkl` artifact + MLflow tracking)
- FastAPI REST API with Swagger UI
- minimal monitoring (logs + counters)
- Docker containerization
- GitHub Actions CI

## Requirements

- Python 3.12+
- Docker

## Local setup (venv)

### Windows (Git Bash)

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
cp .env.example .env
```

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

## Pipeline MLOps

Train and save the model:

```bash
python scripts/train.py
```

The model is stored in `artifacts/model.pkl`.

## Run the API

```bash
uvicorn mlops_api.main:app --app-dir apps/api --host 0.0.0.0 --port 8000
```

Endpoints:
- `GET /health`
- `POST /predict`
- `GET /metrics`

Swagger UI:
- `http://localhost:8000/docs`

Example `POST /predict` payload:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

## Monitoring

- HTTP request logs via middleware
- input/output logs on `/predict`
- counters:
  - total requests
  - total predictions

## Tests

```bash
pytest
```

## Docker

Build image:

```bash
docker build -t ml-api .
```

Run container:

```bash
docker run --rm -p 8000:8000 ml-api
```

With compose:

```bash
docker compose up --build
```

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
- dependency installation
- test execution
- Docker image build
