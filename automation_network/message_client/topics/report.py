import json
import logging

from paho.mqtt.client import MQTTMessage
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.topics.decorators.decode_message import decode
from han_mqtt.security.confirm_client_id import confirm_client_id

from secrets import SECRET_KEY

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report/attach", actions=["message"])
@decode(key=SECRET_KEY)
@confirm_client_id()
def attach(message: MQTTMessage, **_):
    LOG.info(f"{json.dumps(message.payload, indent=4)}")
