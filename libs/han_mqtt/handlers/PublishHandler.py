import json
import logging
from typing import Any, Callable, Dict, List, Optional

from paho.mqtt.client import Client as MQTTClient
from paho.mqtt.client import MQTTMessageInfo

from han_mqtt.models.UserData import MqttUserData

LOG = logging.getLogger(__name__)


class PublishHandler:
    def __init__(self, client: MQTTClient):
        self.client = client
        self._topic_handler_map: Dict[str, Dict[int, Callable]] = {}
        self._mid_topic_map: Dict[int, str] = {}

    def add_mid_topic_mapping(self, mid: int, topic: str) -> None:
        self._mid_topic_map[mid] = topic

    def add_topic_publish_handler(self, topic: str, handler: Callable) -> int:
        handler_id: int = 0

        if topic in self._topic_handler_map:
            handler_id = len(self._topic_handler_map)
        else:
            self._topic_handler_map[topic] = {}

        self._topic_handler_map[topic][handler_id] = handler

        return handler_id

    def get_topic_publish_handler(
        self, topic: str, handler_id: int
    ) -> Optional[Callable]:
        return self._topic_handler_map.get(topic, {}).get(handler_id, None)

    def get_topic_publish_handlers(self, topic: str) -> List[Callable]:
        return list(self._topic_handler_map.get(topic, {}).values())

    def remove_topic_publish_handler(self, topic: str, handler_id: int) -> None:
        if self.get_topic_publish_handler(topic=topic, handler_id=handler_id) is not None:
            del self._topic_handler_map[topic][handler_id]

    def publish(
        self,
        topic: str,
        payload: Dict[str, Any] = None,
        qos: int = 0,
        retain: bool = False,
    ) -> MQTTMessageInfo:
        message_info = self.client.publish(
            topic=topic, payload=json.dumps(payload), qos=qos, retain=retain
        )
        self.add_mid_topic_mapping(mid=message_info.mid, topic=topic)

        return message_info

    def handle_publish(
        self, client: MQTTClient, userdata: MqttUserData, mid: int
    ) -> None:
        topic = self._mid_topic_map.get(mid, None)

        if topic is not None:
            for handler in self.get_topic_publish_handlers(topic=topic):
                try:
                    handler(client=client, user_data=userdata, mid=mid)
                except Exception as Error:
                    LOG.exception(Error)

            del self._mid_topic_map[mid]