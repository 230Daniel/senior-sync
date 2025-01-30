import copy
from fastapi.testclient import TestClient
import mongomock
import pytest

from app.main import app
from app.database import get_db, Database

from .constants import TEST_HEART_RATE_DATAPOINTS, TEST_HEART_RATE_SENSOR, TEST_STR_SENSOR

@pytest.fixture(scope="function")
def test_client():
    """
    Fixture for tests that need a test API server.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def test_db():
    """
    Fixture for tests that need a mocked MongoDB connection.
    """
    with mongomock.MongoClient() as client:
        def get_test_db():
            yield Database(client)

        app.dependency_overrides[get_db] = get_test_db
        yield client["senior_sync"]

    app.dependency_overrides.pop(get_db)

@pytest.fixture(scope="function")
def test_sensors(test_db: Database):
    """
    Fixture for tests that expect sensors to exist in the database already.
    """
    sensors = [
        TEST_HEART_RATE_SENSOR,
        TEST_STR_SENSOR
    ]

    test_db.sensors.insert_many(sensors)

    yield sensors

    test_db.sensors.delete_many({ "_id": {
        "$in": [[sensor["_id"] for sensor in sensors]]
    }})

@pytest.fixture(scope="function")
def test_heart_rate_sensor(test_sensors):
    yield TEST_HEART_RATE_SENSOR

@pytest.fixture(scope="function")
def test_heart_rate_datapoints(test_db: Database, test_heart_rate_sensor):
    """
    Fixture for tests that expect sensors to exist in the database already.
    """
    test_db[f"sensor-datapoints-{test_heart_rate_sensor['_id']}"].insert_many(TEST_HEART_RATE_DATAPOINTS)

    yield [
        data_point.pop("_id") and data_point | { "timestamp": data_point["timestamp"].isoformat() }
        for data_point in copy.deepcopy(TEST_HEART_RATE_DATAPOINTS)
    ]

    test_db.sensors.delete_many({ "_id": {
        "$in": [[datapoint["_id"] for datapoint in TEST_HEART_RATE_DATAPOINTS]]
    }})
