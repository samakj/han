import logging
from datetime import datetime

from paho.mqtt.client import MQTTMessage
from han_mqtt.topics.TopicBlueprint import TopicBlueprint

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

DEFAULT_TOPIC_BLUEPRINT = TopicBlueprint()


@DEFAULT_TOPIC_BLUEPRINT.topic("/log", actions=["message"])
def log(message: MQTTMessage, **_):
    LOG.info(f"DEBUG@{datetime.utcnow()}: {message.payload.decode('utf-8')}")
