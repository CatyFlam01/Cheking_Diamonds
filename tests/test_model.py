from src.data_processing import add_features, generate_sample_data
from src.model_training import calculate_metrics, train_model


def test_calculate_metrics_returns_all_required_values():
    metrics = calculate_metrics([100, 200, 300], [110, 190, 310])

    assert set(metrics) == {"rmse", "mae", "r2", "mape"}
    assert metrics["rmse"] > 0
    assert metrics["r2"] > 0.9


def test_train_model_saves_artifacts(tmp_path):
    data = add_features(generate_sample_data(rows=80))
    train_df = data.iloc[:60].reset_index(drop=True)
    test_df = data.iloc[60:].reset_index(drop=True)

    _, metrics = train_model(
        train_df,
        test_df,
        model_path=tmp_path / "model.joblib",
        metrics_path=tmp_path / "metrics.json",
        baseline_path=tmp_path / "baseline.json",
    )

    assert (tmp_path / "model.joblib").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "baseline.json").exists()
    assert metrics["rmse"] > 0
