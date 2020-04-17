from datetime import datetime

from paho.mqtt.client import MQTTMessage
from han_mqtt.topics.TopicBlueprint import TopicBlueprint

DEFAULT_TOPIC_BLUEPRINT = TopicBlueprint()


@DEFAULT_TOPIC_BLUEPRINT.topic("/log", actions=["message"])
def log(message: MQTTMessage, **_):
    print(f"DEBUG@{datetime.utcnow()}: {message.payload.decode('utf-8')}")
