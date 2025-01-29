from typing import Dict, List
from unittest import TestCase
from fastapi.testclient import TestClient
from mongomock import Database

from .constants import TEST_HEART_RATE_SENSOR, TEST_STR_SENSOR

def test_get_sensors(test_client: TestClient, test_sensors: List[Dict]):
    response = test_client.get("/api/sensors")
    assert response.status_code == 200

    TestCase().assertCountEqual(test_sensors, response.json())


def test_get_sensor(test_client: TestClient, test_sensors: List[Dict]):
    for sensor in test_sensors:
        response = test_client.get(f"/api/sensors/{sensor['_id']}")
        assert response.json() == sensor


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
