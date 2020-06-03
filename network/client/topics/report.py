import os
import logging
import requests
from datetime import datetime

from paho.mqtt.client import MQTTMessage
from midge.topics.topic_blueprint import TopicBlueprint

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report/#", actions=["message"])
def handle_report(message: MQTTMessage, **_) -> None:
    _, device_id, metric_name = message.topic.strip("/").split("/")

    LOG.info(f"Handling {metric_name} report from {device_id}.")

    requests.post(
        url=(
            f"{os.environ['DEVICES_API_HOST']}:{os.environ['DEVICES_API_PORT']}"
            f"/v0/reports/"
        ),
        json={
            "device_id": device_id,
            "reported_at": datetime.utcfromtimestamp(message.payload.split(":")[0]),
            "metric_name": metric_name,
            "value": message.payload.split(":")[1],
        }
    )
