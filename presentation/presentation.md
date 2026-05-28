# Automation ML Diamonds - Presentation

## Slide 1. Business Task

Goal: predict the price of a diamond from its physical and quality characteristics.

Input features:

- carat;
- cut;
- color;
- clarity;
- depth;
- table;
- x, y, z dimensions.

Target: `price`

This is a regression task.

## Slide 2. Data

Dataset: Kaggle Diamonds Dataset.

Why this dataset was chosen:

- simple tabular data;
- clear regression target;
- numeric and categorical features;
- easy to explain during a course defense;
- suitable for demonstrating ETL, preprocessing, API, testing, Docker, CI/CD, and monitoring.

If the full Kaggle CSV is missing, the project creates a deterministic sample dataset for local demo and tests.

## Slide 3. ML System Architecture

```text
Raw CSV
-> validation
-> cleaning
-> feature engineering
-> train/test split
-> model training
-> metrics and baseline
-> saved model
-> FastAPI service
```

Feature engineering:

```python
volume = x * y * z
density = carat / (volume + 0.001)
depth_to_width = depth / (x + 0.001)
```

## Slide 4. Model And Metrics

Model: `RandomForestRegressor`

Why this model:

- stable baseline for tabular regression;
- handles non-linear relationships;
- easy to explain;
- does not require heavy optional dependencies.

Current demo metrics:

| Metric | Value |
| --- | ---: |
| RMSE | 589.5855 |
| MAE | 483.1370 |
| R2 | 0.9631 |
| MAPE | 7.0597 |

Metrics are calculated after real model training and are not hardcoded.

## Slide 5. Testing, Docker, CI/CD

Testing:

- `18 passed`;
- tests use small synthetic DataFrames;
- tests cover ETL, feature engineering, model training, API behavior, and monitoring.

Docker:

- `docker compose build`;
- `docker compose up`;
- API runs on port `8000`.

CI/CD:

- GitHub Actions installs dependencies;
- compiles source files;
- runs pytest;
- builds Docker image.

## Slide 6. Monitoring

Monitoring is intentionally lightweight and educational:

- baseline model metrics;
- numeric feature profiles;
- data drift detection by relative mean shift;
- degradation detection by RMSE increase and R2 drop;
- CPU, RAM, and disk usage with `psutil`.

This demonstrates the core monitoring ideas without adding heavy infrastructure.

## Slide 7. Business Conclusion

The project shows a complete educational ML automation workflow:

- data processing is reproducible;
- model metrics are real;
- predictions are available through FastAPI;
- tests and CI/CD reduce manual checking;
- Docker makes the demo easier to reproduce;
- monitoring provides basic visibility into model and infrastructure state.

The project is ready for course submission after adding the GitHub link and required screenshots to the LMS.
