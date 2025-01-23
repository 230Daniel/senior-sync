from collections import defaultdict
from datetime import datetime, timedelta
import logging
from typing import Dict

from wrapt import synchronized

from ..utils import Singleton

from ..database import get_alerts_for_sensor, update_alert

from ..models.alert import Alert
from ..models.sensor import Sensor
from ..models.datapoint import DataPoint

logger = logging.getLogger(__name__)

class AlertGenerator(Singleton):
    def __init__(self):
        self.alerts: Dict[Alert] = defaultdict(lambda sensor_id: next(get_alerts_for_sensor(sensor_id), None))

    @synchronized
    def on_sensor_updated(self, sensor: Sensor, data_point: DataPoint):
        if recent_alert := self.alerts[sensor.id]:
            if recent_alert.is_active and data_point.colour == "green":
                self.deactivate_alert(recent_alert)
                return

        if (data_point.colour == "red" and (not recent_alert or not recent_alert.is_active)):
            self.new_alert(sensor, data_point)

    def new_alert(self, sensor: Sensor, data_point: DataPoint):
        logger.info(f"New alert for {sensor.id}.")

    def deactivate_alert(self, alert: Alert):
        alert.is_active = False
        update_alert(alert)
        logger.info(f"Old alert {alert.id} for {alert.sensor_id} deactivated.")
