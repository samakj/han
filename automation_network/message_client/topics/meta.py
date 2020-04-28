import logging
from time import time

from paho.mqtt.client import MQTTMessage
from han_mqtt import HanMqttClient
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.topics.decorators.decode_message import decode

from secrets import SECRET_KEY

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

META_TOPIC_BLUEPRINT = TopicBlueprint()


@META_TOPIC_BLUEPRINT.topic("/meta", actions=["message"])
@decode(key=SECRET_KEY)
def get_info(message: MQTTMessage, client: HanMqttClient, **_) -> None:
    node_id = message.payload.get('meta', {}).get('id', None)
    request_keys = set(message.payload['k']) if message.payload.get('k', None) is not None else None

    if node_id is None:
        LOG.error(f"Meta requested with invalid request meta.")
        return
    if request_keys is None:
        LOG.error(f"Meta requested with no keys.")
        return

    LOG.info(f"{message.payload['meta']['id']} requested meta data.")

    response_info = {"meta": {"id": message.payload['meta']['id']}}

    if 't' in request_keys:
        response_info['t'] = int(time())

    if not request_keys:
        LOG.error(f"Meta requested with no valid keys.")
        return

    client.coercive_publish("/v0/meta", response_info)
