import os
import logging
import requests

from paho.mqtt.client import MQTTMessage
from midge.topics.topic_blueprint import TopicBlueprint

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

META_TOPIC_BLUEPRINT = TopicBlueprint()


@META_TOPIC_BLUEPRINT.topic("/meta/+/ping", actions=["message"])
def handle_ping(message: MQTTMessage, **_) -> None:
    _, __, device_id, ___ = message.topic.strip("/").split("/")
    isoTimestamp, ____ = message.payload.decode("utf-8").split("|")

    requests.patch(
        url=(
            f"{os.environ['DEVICES_HOST']}:{os.environ['DEVICES_PORT']}"
            f"/v0/devices/{device_id}/"
        ),
        json={
            "latest_ping": isoTimestamp,
        }
    )
