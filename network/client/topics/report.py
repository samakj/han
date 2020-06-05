import os
import logging
import requests

from paho.mqtt.client import MQTTMessage
from midge.topics.topic_blueprint import TopicBlueprint

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report/#", actions=["message"])
def handle_report(message: MQTTMessage, **_) -> None:
    _, __, device_id, metric_name = message.topic.strip("/").split("/")
    isoTimestamp, value = message.payload.decode("utf-8").split("|")

    requests.post(
        url=(
            f"{os.environ['DEVICES_HOST']}:{os.environ['DEVICES_PORT']}"
            f"/v0/reports/"
        ),
        json={
            "device_id": device_id,
            "reported_at": isoTimestamp,
            "metric_name": metric_name,
            "value": value,
        }
    )
