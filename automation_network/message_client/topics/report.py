import logging

from paho.mqtt.client import MQTTMessage
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.topics.decorators.decode_message import decode
from han_mqtt.security.confirm_timestamp import confirm_timestamp

from secrets import SECRET_KEY

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report/#", actions=["message"])
@decode(key=SECRET_KEY)
@confirm_timestamp()
def handle_report(message: MQTTMessage, **_) -> None:
    LOG.info(f"{message.payload['meta']['id']}'s reported to '{message.topic}'.")
