from paho.mqtt.client import MQTTMessage
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.security.decode_message import decode

from config import KEY

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report", actions=["message"])
@decode(key=KEY)
def report(message: MQTTMessage, **_):
    print(f"{message.payload}")
