import logging
from time import time

from paho.mqtt.client import MQTTMessage
from han_mqtt import HanMqttClient, MqttUserData
from han_mqtt.topics.TopicBlueprint import TopicBlueprint

LOG = logging.getLogger(__name__)
META_TOPIC_BLUEPRINT = TopicBlueprint()


@META_TOPIC_BLUEPRINT.topic("/meta", actions=["message"])
def edge_init_meta(message: MQTTMessage, client: HanMqttClient, user_data: MqttUserData) -> None:
    if str(message.payload.decode("utf-8")) == "init":
        name = user_data.client_id or user_data.username if user_data else None
        LOG.info(f"{name or '< unknown >'} requested init meta data.")
        client.publish("/v0/meta", {"timestamp": int(time())})
