import json
import logging

from paho.mqtt.client import MQTTMessage
from han_mqtt.models.UserData import MqttUserData
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.topics.decorators.decode_message import decode

from secrets import SECRET_KEY

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report/attach", actions=["message"])
@decode(key=SECRET_KEY)
def attach(message: MQTTMessage, user_data: MqttUserData, **_):
    LOG.info(
        f"{MqttUserData.client_id if user_data else None} sent this to /report/attach:\n"
        f"{json.dumps(message.payload, indent=4)}"
    )
