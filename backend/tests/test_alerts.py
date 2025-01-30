import copy
from datetime import datetime
from typing import Dict
from unittest import TestCase
from unittest.mock import ANY
from fastapi.testclient import TestClient
from freezegun import freeze_time
from mongomock import Database

from .constants import TEST_ALERTS


@freeze_time(datetime(2025, 1, 1))
def test_get_active_alerts(test_client: TestClient, test_db: Database):
    test_db.alerts.insert_many(copy.deepcopy(TEST_ALERTS))

    response = test_client.get("/alerts")
    assert response.status_code == 200

    expected_alerts = [
        alert | {"timestamp": alert["timestamp"].isoformat()}
        for alert in TEST_ALERTS
        if alert["is_active"]
    ]

    TestCase().assertCountEqual(expected_alerts, response.json())

@freeze_time(datetime(2025, 1, 1))
def test_add_alert(test_client: TestClient, test_db: Database, test_heart_rate_sensor: Dict):
    sensor_id = test_heart_rate_sensor["_id"]

    response = test_client.post(f"/api/metrics/{sensor_id}", json={
        "timestamp": datetime(2025, 1, 1).isoformat(),
        "value": 0
    })
    assert response.status_code == 201

    expected_alerts = [{
        'sensor_id': 'heart_rate',
        'timestamp': datetime(2025, 1, 1, 0, 0),
        'is_active': True,
        'message': 'The Heart Rate sensor detected a dangerous value of 0 BPM.',
        '_id': ANY
    }]

    alerts = list(test_db.alerts.find({}))

    TestCase().assertCountEqual(expected_alerts, alerts)
