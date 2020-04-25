import logging
from time import time

from paho.mqtt.client import MQTTMessage
from han_mqtt import HanMqttClient, MqttUserData
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.topics.json_payload import json_payload

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

META_TOPIC_BLUEPRINT = TopicBlueprint()


@META_TOPIC_BLUEPRINT.topic("/meta", actions=["message"])
@json_payload()
def edge_init_meta(message: MQTTMessage, client: HanMqttClient, user_data: MqttUserData) -> None:
    if message.payload.get("command") == "INIT_META":
        name = user_data.client_id or user_data.username if user_data else None
        LOG.info(f"{name or '< unknown >'} requested init meta data.")
        client.coercive_publish("/v0/meta", {"timestamp": int(time())})
