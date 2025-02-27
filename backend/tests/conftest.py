import copy
from fastapi.testclient import TestClient
import mongomock
import pytest
from pydantic._internal._generate_schema import GenerateSchema
from pydantic_core import core_schema
from botocore.exceptions import ClientError

from app.main import app
from app.database import get_db, Database
from app.services.alert_generator import AlertGenerator, get_alert_generator

from .constants import TEST_HEART_RATE_DATAPOINTS, TEST_HEART_RATE_SENSOR, TEST_STRING_SENSOR

@pytest.fixture(scope="function")
def test_client():
    """
    Fixture for tests that need a test API server.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def mock_boto3(mocker):
    """
    Fixture to force boto3 client invocations to raise an error.
    """
    mocker.patch("boto3.client", side_effect=ClientError({}, "UnitTest"))

@pytest.fixture(scope="function")
def test_db(mock_boto3):
    """
    Fixture for tests that need a mocked MongoDB connection.
    """
    with mongomock.MongoClient() as client:
        def get_test_db():
            yield Database(client)

        def get_test_alert_generator():
            AlertGenerator.clear()
            alert_generator = AlertGenerator(Database(client))
            yield alert_generator


        app.dependency_overrides[get_db] = get_test_db
        app.dependency_overrides[get_alert_generator] = get_test_alert_generator
        yield client["senior_sync"]

    app.dependency_overrides.pop(get_db)
    app.dependency_overrides.pop(get_alert_generator)


@pytest.fixture(scope="function")
def test_sensors(test_db: Database):
    """
    Fixture for tests that expect sensors to exist in the database already.
    """
    sensors = copy.deepcopy([
        TEST_HEART_RATE_SENSOR,
        TEST_STRING_SENSOR
    ])

    test_db.sensors.insert_many(sensors)

    yield sensors


@pytest.fixture(scope="function")
def test_heart_rate_sensor(test_sensors):
    yield copy.deepcopy(TEST_HEART_RATE_SENSOR)


@pytest.fixture(scope="function")
def test_string_sensor(test_sensors):
    yield copy.deepcopy(TEST_STRING_SENSOR)


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


# Fix for PydanticSchemaGenerationError when using Freezegun
initial_match_type = GenerateSchema.match_type
def match_type(self, obj):
    if getattr(obj, "__name__", None) == "datetime":
        return core_schema.datetime_schema()
    return initial_match_type(self, obj)
GenerateSchema.match_type = match_type
