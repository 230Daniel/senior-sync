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
