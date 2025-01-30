from datetime import datetime

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
