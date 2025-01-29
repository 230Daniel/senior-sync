from fastapi.testclient import TestClient
import mongomock
import pytest

from app.main import app

@pytest.fixture(scope="function")
def test_client():
    with mongomock.patch(), TestClient(app) as test_client:
        yield test_client
