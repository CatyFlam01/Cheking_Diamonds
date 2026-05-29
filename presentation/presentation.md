# Automation ML Diamonds - презентация

## Слайд 1. Бизнес-задача

Цель проекта - предсказать цену бриллианта по его физическим и качественным характеристикам.

Входные признаки:

- carat;
- cut;
- color;
- clarity;
- depth;
- table;
- размеры x, y, z.

Целевая переменная: `price`

Тип задачи: регрессия.

## Слайд 2. Данные

Датасет: Kaggle Diamonds Dataset.

Почему выбран этот датасет:

- простые табличные данные;
- понятная целевая переменная;
- есть числовые и категориальные признаки;
- удобно объяснять при техническом обзоре проекта;
- подходит для проверки ETL, preprocessing, API, testing, Docker, CI/CD и monitoring.

Если полный Kaggle CSV отсутствует, проект создает deterministic sample dataset для локального запуска и тестов.

## Слайд 3. Архитектура ML-системы

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

## Слайд 4. Модель и метрики

Модель: `RandomForestRegressor`

Почему эта модель:

- стабильный baseline для tabular regression;
- умеет учитывать нелинейные зависимости;
- легко объясняется;
- не требует тяжелых дополнительных зависимостей.

Текущие метрики на sample dataset:

| Метрика | Значение |
| --- | ---: |
| RMSE | 589.5855 |
| MAE | 483.1370 |
| R2 | 0.9631 |
| MAPE | 7.0597 |

Метрики вычисляются после реального обучения модели и не захардкожены.

Графики для интерпретации модели:

![Predicted vs Actual](../reports/figures/predicted_vs_actual.png)

Predicted vs Actual показывает, насколько близки предсказания модели к реальным значениям цены.

![Feature importance](../reports/figures/feature_importance.png)

Feature importance показывает, какие признаки сильнее всего влияют на предсказание `RandomForestRegressor`.

## Слайд 5. Тестирование, Docker, CI/CD

Тестирование:

- `18 passed`;
- тесты используют небольшие synthetic DataFrame;
- проверяются ETL, feature engineering, model training, API behavior и monitoring.

Docker:

- `docker compose build`;
- `docker compose up`;
- API работает на порту `8000`.

CI/CD:

- GitHub Actions устанавливает зависимости;
- выполняет compile check;
- запускает pytest;
- собирает Docker image.

## Слайд 6. Мониторинг

Monitoring в проекте легкий и встроенный:

- baseline model metrics;
- numeric feature profiles;
- data drift detection по сдвигу среднего значения;
- degradation detection по росту RMSE и падению R2;
- CPU, RAM и disk usage через `psutil`.

Этого достаточно, чтобы показать основные идеи monitoring без тяжелой инфраструктуры.

![Распределение цены](../reports/figures/price_distribution.png)

Распределение `price` помогает контролировать диапазон данных и замечать возможные сдвиги в новых выборках.

## Слайд 7. Выводы для бизнеса

Проект показывает полный workflow автоматизации ML:

- обработка данных воспроизводима;
- метрики модели реальные;
- предсказания доступны через FastAPI;
- tests и CI/CD уменьшают объем ручной проверки;
- Docker упрощает повторный запуск;
- monitoring дает базовую видимость состояния модели и инфраструктуры.

Проект готов к публикации после добавления ссылки на GitHub и нужных скриншотов во внешнюю документацию.
