import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_menu_lists_five_items(client):
    assert len(client.get("/menu").get_json()) == 5


def test_quote_endpoint(client):
    r = client.post("/quote", json={"items": [{"id": "latte", "qty": 2}, {"id": "espresso"}], "coupon": "BREW10"})
    assert r.status_code == 200
    assert r.get_json()["total"] == 475


def test_quote_rejects_unknown_coupon(client):
    r = client.post("/quote", json={"items": [{"id": "latte"}], "coupon": "NOPE"})
    assert r.status_code == 400
