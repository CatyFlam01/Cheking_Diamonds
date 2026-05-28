# Automation ML Diamonds

Учебный MLOps-проект по дисциплине "Автоматизация машинного обучения".
Цель проекта - показать полный воспроизводимый ML pipeline для задачи регрессии:
предсказание цены бриллианта (`price`) по табличным признакам Kaggle Diamonds Dataset.

Проект не претендует на production enterprise-архитектуру. Он сделан так, чтобы локально запускаться, проходить тесты, собираться в Docker и быть понятным для демонстрации.

## Датасет

Основной датасет: [Kaggle Diamonds Dataset](https://www.kaggle.com/datasets/shivam2503/diamonds).

Ожидаемый файл для реального датасета:

```text
data/raw/diamonds.csv
```

Если файла нет, pipeline автоматически создаст небольшой синтетический diamonds-like датасет. Это нужно для воспроизводимого локального запуска, тестов и Docker-сборки без ручной загрузки Kaggle.

## Что реализовано

- ETL: загрузка raw CSV, валидация, очистка, train/test split.
- Feature engineering:
  - `volume = x * y * z`
  - `density = carat / (volume + 0.001)`
  - `depth_to_width = depth / (x + 0.001)`
- ML training: `RandomForestRegressor` внутри `sklearn Pipeline`.
- Метрики: RMSE, MAE, R2, MAPE.
- FastAPI:
  - `/`
  - `/health`
  - `/predict`
  - `/model/info`
- Monitoring:
  - baseline metrics;
  - простой data drift по числовым признакам;
  - degradation detection;
  - CPU/RAM/disk через `psutil`.
- Tests: unit/API/monitoring tests на маленьких synthetic DataFrame.
- Docker: простой образ для запуска API.
- CI/CD: GitHub Actions устанавливает зависимости, запускает pytest и собирает Docker image.

## Структура

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
└── requirements.txt
```

## Локальный запуск

Создать окружение и установить зависимости:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Запустить ETL:

```bash
python -m src.data_processing
```

Обучить модель:

```bash
python -m src.model_training
```

Запустить полный pipeline:

```bash
python run_pipeline.py
```

Запустить API:

```bash
uvicorn src.app:app --reload
```

После запуска API документация доступна по адресу:

```text
http://127.0.0.1:8000/docs
```

Пример запроса к `/predict`:

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

## Тесты

```bash
pytest -v
```

Тесты не требуют полного Kaggle dataset. Они используют маленькие synthetic DataFrame и проверяют ETL, feature engineering, обучение, API и monitoring.

## Docker

Сборка:

```bash
docker compose build
```

Запуск:

```bash
docker compose up
```

API будет доступно на:

```text
http://127.0.0.1:8000
```

## CI/CD

Workflow находится в `.github/workflows/ci-cd.yml`.

Он выполняет:

1. установку Python-зависимостей;
2. запуск `pytest -v`;
3. сборку Docker image.

Реальный deploy, secrets и внешняя инфраструктура намеренно не добавлены, чтобы проект оставался простым и учебным.
