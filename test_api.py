from fastapi.testclient import TestClient

from main import ALLOWED_ORIGIN, EMAIL, app

client = TestClient(app)


def check_common_headers(response):
    assert response.headers["x-request-id"]
    assert float(response.headers["x-process-time"]) >= 0


def test_stats():
    response = client.get("/stats?values=1,-2,5,10")
    assert response.status_code == 200
    assert response.json() == {
        "email": EMAIL, "count": 4, "sum": 14,
        "min": -2, "max": 10, "mean": 3.5,
    }
    check_common_headers(response)


def test_allowed_preflight():
    response = client.options("/stats?values=1,2", headers={
        "Origin": ALLOWED_ORIGIN,
        "Access-Control-Request-Method": "GET",
    })
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    check_common_headers(response)


def test_disallowed_preflight():
    response = client.options("/stats", headers={
        "Origin": "https://not-allowed.example.com",
        "Access-Control-Request-Method": "GET",
    })
    assert "access-control-allow-origin" not in response.headers
    check_common_headers(response)


def test_invalid_values():
    response = client.get("/stats?values=1,abc")
    assert response.status_code == 400
    check_common_headers(response)


def test_disallowed_simple_get():
    response = client.get("/stats?values=3", headers={
        "Origin": "https://not-allowed.example.com",
    })
    assert "access-control-allow-origin" not in response.headers
    check_common_headers(response)
