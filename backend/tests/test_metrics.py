import copy
from datetime import datetime
from itertools import chain
from operator import itemgetter
from typing import Dict, List
from unittest import TestCase
from unittest.mock import ANY
from fastapi.testclient import TestClient
from mongomock import Database

from .constants import TEST_CREATE_HEART_RATE_DATAPOINT, TEST_HEART_RATE_DATAPOINT, TEST_HEART_RATE_SENSOR


def test_add_datapoint(test_client: TestClient, test_db: Database, test_heart_rate_sensor: Dict):
    # TODO: Loop and create/test all
    sensor_id = test_heart_rate_sensor['_id']
    response = test_client.post(f"/api/metrics/{sensor_id}", json=TEST_CREATE_HEART_RATE_DATAPOINT)
    assert response.status_code == 201

    data_points = list(test_db[f"sensor-datapoints-{sensor_id}"].find({}))

    assert len(data_points) == 1
    assert data_points[0] == TEST_HEART_RATE_DATAPOINT | {
        "_id": ANY
    }


def test_get_datapoints(test_client: TestClient, test_heart_rate_sensor: Dict, test_heart_rate_datapoints: List[Dict]):
    sensor_id = test_heart_rate_sensor['_id']

    
    for start, end in chain.from_iterable(
            [(datetime(2025, 1, i), datetime(2025, 1, j)) for i in range (1, j)] for j in range(1, 6)
        ):
        expected_datapoints = [
            datapoint for datapoint in test_heart_rate_datapoints
            if start.isoformat() <= datapoint["timestamp"] <= end.isoformat()
        ]

        response = test_client.get(f"/api/metrics/{sensor_id}/history", params={
            "start_time": start.isoformat(),
            "end_time": end.isoformat()
        })
        assert response.status_code == 200

        TestCase().assertCountEqual(expected_datapoints, response.json())


def test_get_all(test_client: TestClient, test_sensors: List[Dict], test_heart_rate_datapoints: List[Dict]):
    response = test_client.get(f"/api/metrics/all")
    assert response.status_code == 200

    expected_response = copy.deepcopy(test_sensors)

    for sensor in expected_response:
        if sensor["_id"] == TEST_HEART_RATE_SENSOR["_id"]:
            sensor["value"] = max(test_heart_rate_datapoints, key=itemgetter("timestamp"))
        else:
            sensor["value"] = None

    TestCase().assertCountEqual(expected_response, response.json())

