import logging
from typing import Any, Callable, Dict, List, Optional

from paho.mqtt.client import Client as MQTTClient, MQTTMessage


LOG = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, client):
        self.client = client
        self._topic_handler_map: Dict[str, Dict[int, Callable]] = {}

    def add_topic_message_handler(self, topic: str, handler: Callable) -> int:
        handler_id: int = 0

        if topic in self._topic_handler_map:
            handler_id = len(self._topic_handler_map)
        else:
            self._topic_handler_map[topic] = {}

        self._topic_handler_map[topic][handler_id] = handler

        return handler_id

    def get_topic_message_handler(
        self, topic: str, handler_id: int
    ) -> Optional[Callable]:
        return self._topic_handler_map.get(topic, {}).get(handler_id, None)

    def get_topic_message_handlers(self, topic: str) -> List[Callable]:
        handlers = []

        handlers.extend(self._topic_handler_map.get(topic, {}).values())

        topic_split = topic.split("/")

        while topic_split:
            topic_split[-1] = "#"
            handlers.extend(self._topic_handler_map.get("/".join(topic_split), {}).values())
            del topic_split[-1]

        return handlers

    def remove_topic_message_handler(self, topic: str, handler_id: int) -> None:
        if self.get_topic_message_handler(topic=topic, handler_id=handler_id) is not None:
            del self._topic_handler_map[topic][handler_id]

    def handle_message(
        self, _: MQTTClient, message: MQTTMessage, userdata: Optional[Dict[str, Any]] = None,
    ) -> None:
        for handler in self.get_topic_message_handlers(topic=message.topic):
            try:
                handler(client=self.client, user_data=userdata, message=message)
            except Exception as Error:
                LOG.exception(Error)
