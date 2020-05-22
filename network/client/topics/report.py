import logging

from paho.mqtt.client import MQTTMessage
from han_mqtt.topics.TopicBlueprint import TopicBlueprint

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report/#", actions=["message"])
def handle_report(message: MQTTMessage, **_) -> None:
    node_id = message.payload.get('_id', None)

    if node_id is None:
        LOG.error(f"Meta requested with invalid request meta: \n{message.payload}")

    LOG.info(f"{message.payload['_id']} reported to '{message.topic}'.")
