import pytest
from fastapi.testclient import TestClient

from backend import main, utils


@pytest.fixture()
def client():
    return TestClient(main.app)


# --------- Mock helpers ----------
def fake_retrieve_chunks(query, client, conn):
    return [
        (None, None, "Sleep supports cardiovascular health.", "CDC Sleep & Heart", "https://example.com/cdc", 0.88),
        (None, None, "Adults generally need 7+ hours of sleep.", "CDC Sleep", "https://example.com/sleep", 0.84),
    ]


def fake_generate_answer(client, prompt):
    return "Sleep is important for heart health because it supports recovery and cardiovascular function. (CDC Sleep)"


def fake_fetch_metrics_summary(conn, user_id, days):
    if user_id == "00000000-0000-0000-0000-000000000000":
        return None
    return {
        "avg_sleep": 395,
        "avg_resting_hr": 68.2,
        "avg_hrv": 42.0,
        "total_steps": 54000,
        "sleep_variability": 62.0,
    }


def fake_should_use_metrics(message: str) -> bool:
    return True


def fake_compute_health_flags(summary):
    return ["low_sleep", "elevated_rhr"]


class DummyConn:
    def close(self):  
        pass


def fake_get_db_conn():
    return DummyConn()


class DummyOpenAIClient:
    pass


def fake_get_openai_client():
    return DummyOpenAIClient()


# --------- Tests ----------
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}


def test_rag_answer_missing_question(client):
    r = client.post("/rag/answer", json={})
    assert r.status_code == 400
    assert "Missing 'question'" in r.text


def test_rag_answer_success(client, monkeypatch):
    monkeypatch.setattr(main, "get_db_conn", fake_get_db_conn)
    monkeypatch.setattr(main, "get_openai_client", fake_get_openai_client)
    monkeypatch.setattr(utils, "retrieve_chunks", fake_retrieve_chunks)
    monkeypatch.setattr(utils, "generate_answer", fake_generate_answer)

    r = client.post("/rag/answer", json={"question": "Why is sleep important?"})
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert "citations" in data
    assert data["confidence"] > 0
    assert len(data["citations"]) >= 1


def test_metrics_summary_404(client, monkeypatch):
    monkeypatch.setattr(main, "get_db_conn", fake_get_db_conn)
    monkeypatch.setattr(utils, "fetch_metrics_summary", fake_fetch_metrics_summary)

    r = client.get("/metrics/summary", params={"user_id": "00000000-0000-0000-0000-000000000000", "days": 7})
    assert r.status_code == 404


def test_metrics_summary_success(client, monkeypatch):
    monkeypatch.setattr(main, "get_db_conn", fake_get_db_conn)
    monkeypatch.setattr(utils, "fetch_metrics_summary", fake_fetch_metrics_summary)

    r = client.get("/metrics/summary", params={"user_id": "11111111-1111-1111-1111-111111111111", "days": 7})
    assert r.status_code == 200
    data = r.json()
    assert data["summary"]["avg_sleep"] == 395


def test_metrics_compare_success(client, monkeypatch):
    monkeypatch.setattr(main, "get_db_conn", fake_get_db_conn)
    monkeypatch.setattr(utils, "fetch_metrics_summary", fake_fetch_metrics_summary)

    r = client.get("/metrics/compare", params={"user_id": "11111111-1111-1111-1111-111111111111", "days": 7, "baseline_days": 30})
    assert r.status_code == 200
    data = r.json()
    assert "changes" in data
    assert "sleep_change_pct" in data["changes"]


def test_chat_missing_fields(client):
    r = client.post("/chat", json={"user_id": "x"})
    assert r.status_code == 400


def test_chat_success(client, monkeypatch):
    monkeypatch.setattr(main, "get_db_conn", fake_get_db_conn)
    monkeypatch.setattr(main, "get_openai_client", fake_get_openai_client)
    monkeypatch.setattr(utils, "fetch_metrics_summary", fake_fetch_metrics_summary)
    monkeypatch.setattr(utils, "should_use_metrics", fake_should_use_metrics)
    monkeypatch.setattr(utils, "compute_health_flags", fake_compute_health_flags)
    monkeypatch.setattr(utils, "retrieve_chunks", fake_retrieve_chunks)
    monkeypatch.setattr(utils, "generate_answer", fake_generate_answer)

    r = client.post("/chat", json={
        "user_id": "11111111-1111-1111-1111-111111111111",
        "message": "Why am I tired lately?",
        "days": 7,
        "baseline_days": 30
    })
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert "metrics" in data
    assert "flags" in data
    assert len(data["citations"]) >= 1