import json
import jwt
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
    node_id = message.payload.get('_id', None)
    request_keys = set(message.payload['k']) if message.payload.get('k', None) is not None else None

    if node_id is None:
        LOG.error(f"Meta requested with invalid request meta: \n{json.dumps(message.payload)}")
        return
    if request_keys is None:
        LOG.error(f"{message.payload['_id']} requested meta with no keys: \n{json.dumps(message.payload)}")
        return

    LOG.info(f"{message.payload['_id']} requested meta data.")

    response_info = {"_id": message.payload['_id']}

    if 't' in request_keys:
        response_info['t'] = int(time())

    if not request_keys:
        LOG.error(f"{message.payload['_id']} requested meta with no valid keys: \n{json.dumps(message.payload)}")
        return

    client.coercive_publish("/v0/meta", jwt.encode(response_info, key=SECRET_KEY))
