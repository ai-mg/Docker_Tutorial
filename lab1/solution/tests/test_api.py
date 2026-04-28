"""Smoke tests. Run from the host with:

    pip install httpx pytest
    docker compose up -d
    pytest tests/
"""
import httpx

BASE_URL = "http://localhost:8000"


def test_health() -> None:
    r = httpx.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_predict_setosa() -> None:
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    r = httpx.post(f"{BASE_URL}/predict", json=payload, timeout=5)
    assert r.status_code == 200
    body = r.json()
    assert body["species"] == "setosa"
    assert sum(body["probabilities"].values()) == \
        round(sum(body["probabilities"].values()), 6)


def test_predictions_endpoint() -> None:
    r = httpx.get(f"{BASE_URL}/predictions", timeout=5)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
