import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("helpdesk_app", Path(__file__).parents[1] / "app" / "app.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
app = module.app


def test_healthz():
    client = app.test_client()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json()["status"] == "alive"


def test_home_route_exists_even_if_db_is_unavailable():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Kubernetes Help Desk" in response.data


def test_ready_is_success_or_dependency_failure():
    client = app.test_client()
    response = client.get("/ready")
    assert response.status_code in (200, 503)
    assert "status" in response.get_json()
