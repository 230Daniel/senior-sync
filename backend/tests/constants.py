from datetime import datetime, timedelta

TEST_HEART_RATE_SENSOR = {
    "_id": "heart_rate",
    "friendly_name": "Heart Rate",
    "unit": "BPM",
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

TEST_STRING_SENSOR = {
    "_id": "test_str_sensor",
    "friendly_name": "Test String Sensor",
    "unit": "passes",
    "value_type": "str",
    "colour_status_boundaries": None
}

TEST_HEART_RATE_DATAPOINTS = [
    {
        "_id": 1,
        "timestamp": datetime(2025, 1, 1),
        "value": 120,
        "colour": "green"
    },
    {
        "_id": 2,
        "timestamp": datetime(2025, 1, 2),
        "value": 0,
        "colour": "red"
    },
    {
        "_id": 3,
        "timestamp": datetime(2025, 1, 3),
        "value": 170,
        "colour": "amber"
    },
    {
        "_id": 4,
        "timestamp": datetime(2025, 1, 4),
        "value": 60,
        "colour": "green"
    },
    {
        "_id": 5,
        "timestamp": datetime(2025, 1, 5),
        "value": 9000,
        "colour": "red"
    },
    {
        "_id": 6,
        "timestamp": datetime(2025, 1, 6),
        "value": -18,
        "colour": "red"
    }
]

TEST_STRING_DATAPOINTS = [
    {
        "_id": 1,
        "timestamp": datetime(2025, 1, 1),
        "value": "silent but deadly",
        "colour": None
    },
    {
        "_id": 2,
        "timestamp": datetime(2025, 1, 2),
        "value": "oh god",
        "colour": None
    },
    {
        "_id": 3,
        "timestamp": datetime(2025, 1, 3),
        "value": "my eyes",
        "colour": None
    },
    {
        "_id": 4,
        "timestamp": datetime(2025, 1, 4),
        "value": "surprisingly tame",
        "colour": None
    }
]

TEST_ALERTS = [
    {
        "sensor_id": "test_active_sensor",
        "timestamp": datetime(2025, 1, 1),
        "is_active": True,
        "message": "Test active alert message"
    },
    {
        "sensor_id": "test_inactive_sensor",
        "timestamp": datetime(2025, 1, 1) - timedelta(hours=1),
        "is_active": False,
        "message": "Test active non-active message"
    }
]

HEART_RATE_ALERT = {
    'sensor_id': 'heart_rate',
    'timestamp': datetime(2025, 1, 1, 0, 0),
    'is_active': True,
    'message': 'The Heart Rate sensor detected a dangerous value of 0 BPM.'
}
