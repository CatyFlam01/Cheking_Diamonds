# Automation ML Diamonds - Presentation Notes

## 1. Project Topic

Prediction of diamond price using a tabular regression model and a reproducible MLOps pipeline.

Course focus: automation of machine learning, not only model training.

## 2. Why Diamonds Dataset

- Simple and understandable tabular data.
- Clear regression target: `price`.
- Mix of numeric and categorical features.
- Good fit for demonstrating ETL, preprocessing, feature engineering, API, tests, Docker, CI/CD, and monitoring.
- Less complex than NLP, so the project can focus on MLOps workflow quality.

Dataset source: Kaggle Diamonds Dataset.

## 3. Business Task

Given diamond characteristics:

- carat;
- cut;
- color;
- clarity;
- depth;
- table;
- x, y, z dimensions;

predict the expected price of a diamond.

## 4. ML Pipeline

```text
Raw CSV
-> validation
-> cleaning
-> feature engineering
-> train/test split
-> model training
-> metrics
-> saved model
-> FastAPI prediction service
```

Feature engineering:

```python
volume = x * y * z
density = carat / (volume + 0.001)
depth_to_width = depth / (x + 0.001)
```

## 5. Model

Model: `RandomForestRegressor`

Why this model:

- stable baseline for tabular regression;
- works well with non-linear relationships;
- easy to explain;
- available in scikit-learn;
- does not require heavy optional dependencies.

## 6. Current Metrics

Metrics are calculated after real training, not hardcoded.

Current demo metrics on the generated sample dataset:

| Metric | Value |
| --- | ---: |
| RMSE | 589.5855 |
| MAE | 483.1370 |
| R2 | 0.9631 |
| MAPE | 7.0597 |

If the full Kaggle CSV is used, metrics may change.

## 7. API

FastAPI endpoints:

- `GET /` - API entry point.
- `GET /health` - health status, model status, CPU/RAM/disk metrics.
- `POST /predict` - diamond price prediction.
- `GET /model/info` - model path, metrics, and feature list.

Important behavior:

- API import does not fail if model is missing.
- `/predict` returns HTTP 503 with a clear message if the model has not been trained.
- Input validation is handled by Pydantic/FastAPI.

## 8. Testing

Tests use small synthetic DataFrames, so they do not require the full Kaggle dataset.

Covered areas:

- data validation;
- cleaning;
- feature engineering;
- model training artifacts;
- metrics calculation;
- API success path;
- API failure path without model;
- API input validation;
- data drift detection;
- degradation detection;
- infrastructure metrics.

Current result:

```text
18 passed
```

## 9. Monitoring

Monitoring is lightweight and educational:

- baseline model metrics are saved;
- numeric feature profiles are saved;
- data drift is detected by relative mean shift;
- degradation is detected by RMSE increase and R2 drop;
- infrastructure metrics are collected with `psutil`.

This is not a production monitoring platform, but it demonstrates the main MLOps monitoring ideas clearly.

## 10. Docker

Docker demonstrates reproducible environment setup:

- installs dependencies;
- runs ETL and model training during image build;
- starts FastAPI on port `8000`;
- includes a container healthcheck.

Main commands:

```bash
docker compose build
docker compose up
```

## 11. CI/CD

GitHub Actions workflow:

- checks out the repository;
- sets up Python;
- uses pip cache;
- installs dependencies;
- compiles Python source files;
- runs pytest;
- builds Docker image.

There is no deploy step because this is a course project and should remain easy to run locally.

## 12. What Was Automated

- Raw data handling with fallback sample generation.
- ETL pipeline.
- Feature engineering.
- Model training.
- Metric calculation.
- Baseline monitoring artifact creation.
- API service startup.
- Test execution.
- Docker image build.
- CI workflow checks.

## 13. What Was Difficult

- Keeping the project useful without overcomplicating it.
- Making tests independent from the full Kaggle dataset.
- Ensuring API imports safely before model training.
- Keeping Docker simple while still demonstrating a full ML workflow.
- Avoiding fake metrics or fake monitoring.

## 14. Conclusion

The project demonstrates a complete educational ML automation pipeline:

- reproducible ETL;
- preprocessing and feature engineering;
- real model training;
- real metrics;
- FastAPI inference;
- tests;
- Docker;
- CI/CD;
- monitoring;
- documentation.

The repository is ready for course demonstration and can be extended later with richer model comparison, coverage reporting, or a monitoring dashboard.
