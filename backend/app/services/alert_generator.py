from datetime import datetime, timedelta
import logging
import os
from urllib.parse import urljoin

from wrapt import synchronized

from .email_sender import EmailSender
from ..utils import Singleton, to_human_time
from ..database import add_alert, get_active_alerts_for_sensor, update_alert

from ..models.alert import Alert
from ..models.sensor import Sensor
from ..models.datapoint import DataPoint

FRONTEND_URL = os.getenv("CORS_ALLOWED_ORIGINS")

class AlertGenerator(Singleton):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_sender = EmailSender.create_email_sender()

    @synchronized
    def on_sensor_updated(self, sensor: Sensor, data_point: DataPoint):
        if recent_alert := next(iter(get_active_alerts_for_sensor(sensor.id)), None):
            if data_point.colour == "green":
                self.deactivate_alert(recent_alert)
            return

        if data_point.colour == "red" and data_point.timestamp > datetime.now() - timedelta(minutes=1):
            self.new_alert(sensor, data_point)

    def new_alert(self, sensor: Sensor, data_point: DataPoint):
        self.logger.info(f"New alert for {sensor.id}.")

        alert = Alert(
            sensor_id = sensor.id,
            timestamp = datetime.now(),
            is_active=True,
            message=f"The {sensor.friendly_name} sensor detected a dangerous value of {data_point.value} {sensor.unit}."
        )

        add_alert(alert)

        sensor_url = urljoin(FRONTEND_URL, f"/metric/{sensor.id}")
        alerts_url = urljoin(FRONTEND_URL, f"/alerts")

        self.email_sender.send_email(
            subject=f"ALERT: {alert.message}",
            body=(
                "Hello,\n\n",
                f"On {to_human_time(data_point.timestamp)}, the {sensor.friendly_name} sensor "
                f"detected a dangerous value of {data_point.value} {sensor.unit}.\n\n"
                f"Find more details about this sensor at {sensor_url}.\n"
                f"Check your alerts at {alerts_url}.\n\n"
                f"The Senior Sync Team."
            )
        )

    def deactivate_alert(self, alert: Alert):
        alert.is_active = False
        update_alert(alert)
        self.logger.info(f"Old alert {alert.id} for {alert.sensor_id} deactivated.")
