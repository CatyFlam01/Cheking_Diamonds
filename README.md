# Automation ML Diamonds

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-pytest-green)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/docker-compose-blue)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

Educational MLOps project for the course "Automation of Machine Learning".

The project demonstrates a complete, reproducible ML workflow for a tabular regression task: predicting diamond price (`price`) from the Kaggle Diamonds dataset.

This is intentionally a course/demo project, not an enterprise production system. The focus is on stability, clarity, local reproducibility, tests, Docker, CI/CD, and explainable project structure.

## Project Goal

Predict diamond price using these input features:

- `carat`
- `cut`
- `color`
- `clarity`
- `depth`
- `table`
- `x`
- `y`
- `z`

Target: `price`

Task type: regression

Dataset: [Kaggle Diamonds Dataset](https://www.kaggle.com/datasets/shivam2503/diamonds)

## Pipeline Diagram

```mermaid
flowchart LR
    A["Raw CSV<br/>data/raw/diamonds.csv"] --> B["Validation"]
    B --> C["Cleaning"]
    C --> D["Feature Engineering<br/>volume, density, depth_to_width"]
    D --> E["Train/Test Split"]
    E --> F["Model Training<br/>RandomForestRegressor"]
    F --> G["Metrics<br/>RMSE, MAE, R2, MAPE"]
    F --> H["Saved Model<br/>models/diamond_price_model.joblib"]
    G --> I["Monitoring Baseline"]
    H --> J["FastAPI<br/>/predict, /health, /model/info"]
    I --> J
```

## What Is Implemented

- ETL pipeline with validation, cleaning, feature engineering, and processed data output.
- Real model training with `RandomForestRegressor`.
- Real metrics calculated after training: RMSE, MAE, R2, MAPE.
- FastAPI service with health, prediction, and model information endpoints.
- Lightweight monitoring:
  - baseline metrics;
  - numeric data drift;
  - model degradation detection;
  - CPU/RAM/disk usage with `psutil`.
- Tests using small synthetic DataFrames, so the full Kaggle dataset is not required.
- Docker and Docker Compose configuration.
- GitHub Actions workflow for tests and Docker image build.

## Project Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── app.py
│   ├── data_processing.py
│   ├── infrastructure_monitoring.py
│   ├── model_training.py
│   └── monitoring.py
├── tests/
│   ├── test_api.py
│   ├── test_data.py
│   ├── test_model.py
│   └── test_monitoring.py
├── docker/
│   ├── Dockerfile
│   └── prometheus.yml
├── .github/workflows/
│   └── ci-cd.yml
├── models/
├── reports/
│   ├── figures/
│   └── monitoring/
├── presentation/
├── run_pipeline.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick Start

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full ML pipeline:

```bash
python run_pipeline.py
```

Expected output:

```text
Pipeline completed
rmse: 589.5855
mae: 483.1370
r2: 0.9631
mape: 7.0597
```

The exact values can differ if you replace the generated sample data with the full Kaggle dataset.

## Dataset Setup

For the real Kaggle dataset, place the CSV here:

```text
data/raw/diamonds.csv
```

If the file is missing, the project automatically creates a small deterministic diamonds-like sample dataset. This keeps tests, Docker builds, and local demos reproducible without manual Kaggle download.

## Running ETL

```bash
python -m src.data_processing
```

Expected output:

```text
Saved processed train/test data: train=400, test=100
```

Generated files:

- `data/raw/diamonds.csv` if no raw dataset existed;
- `data/processed/train.csv`;
- `data/processed/test.csv`;
- `data/processed/diamonds_processed.csv`.

## Training

```bash
python -m src.model_training
```

Expected output is a JSON object with real metrics:

```json
{
  "rmse": 589.5855030260885,
  "mae": 483.1369603844399,
  "r2": 0.9631170911086028,
  "mape": 7.059739162247627
}
```

Generated files:

- `models/diamond_price_model.joblib`;
- `models/metrics.json`;
- `reports/monitoring/baseline.json`.

## API

Start FastAPI locally:

```bash
uvicorn src.app:app --reload
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

- `GET /` - basic API message.
- `GET /health` - service and model status plus infrastructure metrics.
- `POST /predict` - predict diamond price.
- `GET /model/info` - model path, feature list, and saved metrics.

Example request body for `POST /predict`:

```json
{
  "carat": 1.0,
  "cut": "Ideal",
  "color": "E",
  "clarity": "VS1",
  "depth": 61.0,
  "table": 57.0,
  "x": 6.0,
  "y": 6.1,
  "z": 3.8
}
```

Example response:

```json
{
  "predicted_price": 6100.25
}
```

If the model has not been trained yet, `/predict` returns HTTP 503 with an instruction to run training first. Importing the API does not crash when the model is absent.

## Tests

Run all tests:

```bash
pytest -v
```

Expected current result:

```text
18 passed
```

The tests cover:

- data validation;
- cleaning;
- feature engineering;
- metric calculation;
- model artifact saving;
- API health/info/prediction;
- data drift;
- degradation detection;
- infrastructure monitoring metrics.

Optional coverage command if `pytest-cov` is installed:

```bash
pytest --cov=src --cov-report=term-missing
```

Recommended coverage scope:

- keep synthetic tests small and deterministic;
- cover ETL, feature engineering, API success/failure paths, training, and monitoring;
- avoid requiring the full Kaggle CSV in CI.

## Monitoring

Print current infrastructure metrics:

```bash
python -m src.infrastructure_monitoring
```

Example output:

```json
{
  "cpu_percent": 10.5,
  "ram_percent": 88.4,
  "disk_percent": 43.4
}
```

Monitoring is intentionally lightweight and educational. It is enough to demonstrate baseline metrics, drift checks, degradation checks, and system resource checks without requiring external services.

## Docker

Build the image:

```bash
docker compose build
```

Run the API:

```bash
docker compose up
```

Expected behavior:

- the image installs Python dependencies;
- the image runs ETL and model training during build so the API has a model artifact inside the image;
- the API starts on port `8000`;
- docs are available at `http://127.0.0.1:8000/docs`.

If Docker Engine is not running, start Docker Desktop first and retry.

## CI/CD

GitHub Actions workflow:

```text
.github/workflows/ci-cd.yml
```

It performs:

1. repository checkout;
2. Python setup;
3. dependency installation;
4. `pytest -v`;
5. Docker image build.

There is no deploy step, cloud integration, or secrets usage. This is intentional for a stable public course repository.

## Troubleshooting

### `ModuleNotFoundError`

Install dependencies in the active environment:

```bash
pip install -r requirements.txt
```

### `/predict` returns HTTP 503

Train the model first:

```bash
python -m src.model_training
```

### Kaggle dataset is missing

This is safe. The project will generate a deterministic sample dataset automatically. To use the real data, place `diamonds.csv` in `data/raw/`.

### Docker build fails because Docker Engine is unavailable

Start Docker Desktop, wait until the engine is running, then retry:

```bash
docker compose build
```

## Submission Notes

This repository demonstrates the requested educational MLOps components:

- ETL;
- preprocessing;
- model training;
- real metrics;
- API;
- tests;
- Docker;
- CI/CD;
- monitoring;
- documentation.

Future improvements could include a richer dashboard, model comparison, and coverage publishing, but those are intentionally outside the current course-demo scope.
