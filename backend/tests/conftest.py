from fastapi.testclient import TestClient
import mongomock
import pytest

from app.main import app
from app.database import get_db, Database

@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def test_db():
    with mongomock.MongoClient() as client:
        def get_test_db():
            yield Database(client)

        app.dependency_overrides[get_db] = get_test_db
        yield client["senior_sync"]

    app.dependency_overrides.pop(get_db)
