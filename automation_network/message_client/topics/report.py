from paho.mqtt.client import MQTTMessage
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.security.decode_message import decode

from secrets import SECRET_KEY

REPORT_TOPIC_BLUEPRINT = TopicBlueprint()


@REPORT_TOPIC_BLUEPRINT.topic("/report", actions=["message"])
@decode(key=SECRET_KEY)
def report(message: MQTTMessage, **_):
    print(f"{message.payload}")
