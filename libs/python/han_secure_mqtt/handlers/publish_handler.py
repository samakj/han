import json
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from paho.mqtt.client import Client as MQTTClient
from han_secure_mqtt.models.user_data import HanMqttUserData
from han_secure_mqtt.models.message_info import HanMqttMessageInfo

LOG = logging.getLogger(__name__)


class PublishHandler:
    def __init__(self, client):
        self.client = client
        self._topic_handler_map: Dict[str, Dict[int, Callable]] = {}
        self._mid_topic_map: Dict[int, str] = {}

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
        handlers = []

        handlers.extend(self._topic_handler_map.get(topic, {}).values())

        topic_split = topic.split("/")

        while topic_split:
            topic_split[-1] = "#"
            handlers.extend(self._topic_handler_map.get("/".join(topic_split), {}).values())
            del topic_split[-1]

        return handlers

    def remove_topic_publish_handler(self, topic: str, handler_id: int) -> None:
        if self.get_topic_publish_handler(topic=topic, handler_id=handler_id) is not None:
            del self._topic_handler_map[topic][handler_id]

    def publish(
        self,
        topic: str,
        payload: Optional[Union[Dict[str, Any], str, int]] = None,
        qos: int = 0,
        retain: bool = False,
    ) -> HanMqttMessageInfo:
        message_info = super(type(self.client), self.client).publish(
            topic=topic,
            payload=json.dumps(payload) if isinstance(payload, dict) else payload,
            qos=qos,
            retain=retain
        )
        self._mid_topic_map[message_info.mid] = topic

        return message_info

    def handle_publish(
        self, _: MQTTClient, userdata: HanMqttUserData, mid: int
    ) -> None:
        topic = self._mid_topic_map.get(mid, None)
        userdata = userdata or HanMqttUserData()

        if topic is not None:
            for handler in self.get_topic_publish_handlers(topic=topic):
                try:
                    handler(client=self.client, user_data=userdata, mid=mid)
                except Exception as Error:
                    LOG.exception(Error)

            del self._mid_topic_map[mid]
