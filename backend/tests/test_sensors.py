from unittest import TestCase
from fastapi.testclient import TestClient
from mongomock import Database

TEST_HEART_RATE_SENSOR = {
    "_id": "heart_rate",
    "friendly_name": "Heart Rate",
    "unit": "passes",
    "value_type": "int",
    "colour_status_boundaries": [
        {
            "threshold": 0,
            "colour": "red"
        },
        {
            "threshold": 30,
            "colour": "amber"
        },
        {
            "threshold": 50,
            "colour": "green"
        },
        {
            "threshold": 150,
            "colour": "amber"
        },
        {
            "threshold": 200,
            "colour": "red"
        }
    ]
}

TEST_STR_SENSOR = {
    "_id": "test_str_sensor",
    "friendly_name": "Test String Sensor",
    "unit": "passes",
    "value_type": "str",
    "colour_status_boundaries": None
}


def test_get_sensors(test_client: TestClient, test_db: Database):
    sensors = [
        TEST_HEART_RATE_SENSOR,
        TEST_STR_SENSOR
    ]
    test_db.sensors.insert_many(sensors)

    response = test_client.get("/api/sensors")
    assert response.status_code == 200

    TestCase().assertCountEqual(sensors, response.json())


def test_get_sensor(test_client: TestClient, test_db: Database):
    sensors = [
        TEST_HEART_RATE_SENSOR,
        TEST_STR_SENSOR
    ]
    test_db.sensors.insert_many(sensors)

    response = test_client.get(f"/api/sensors/{TEST_HEART_RATE_SENSOR['_id']}")
    assert response.json() == TEST_HEART_RATE_SENSOR

    response = test_client.get(f"/api/sensors/{TEST_STR_SENSOR['_id']}")
    assert response.json() == TEST_STR_SENSOR


def test_add_str_sensor(test_client: TestClient, test_db: Database):
    response = test_client.post("/api/sensors", json=TEST_STR_SENSOR)
    assert response.status_code == 201

    sensors = list(test_db.sensors.find({}))

    assert len(sensors) == 1
    assert sensors[0] == TEST_STR_SENSOR | {
        "colour_status_boundaries": None
    }


def test_add_heart_rate_sensor(test_client: TestClient, test_db: Database):
    response = test_client.post("/api/sensors", json=TEST_HEART_RATE_SENSOR)
    assert response.status_code == 201

    sensors = list(test_db.sensors.find({}))

    assert len(sensors) == 1
    assert sensors[0] == TEST_HEART_RATE_SENSOR
