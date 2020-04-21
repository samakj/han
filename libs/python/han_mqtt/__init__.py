import logging
from typing import Any, Callable, Dict

from paho.mqtt.client import Client as MQTTClient
from paho.mqtt.client import MQTTMessageInfo

from han_mqtt.handlers.ConnectionHandler import ConnectionHandler
from han_mqtt.handlers.MessageHandler import MessageHandler
from han_mqtt.handlers.PublishHandler import PublishHandler
from han_mqtt.handlers.SubscriptionHandler import SubscriptionHandler
from han_mqtt.models.UserData import MqttUserData
from han_mqtt.topics.TopicBlueprint import TopicBlueprint
from han_mqtt.topics.default_topics import DEFAULT_TOPIC_BLUEPRINT

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class HanMqttClient(MQTTClient):
    def __init__(
        self, client_id: str, host: str, port: int, user_data: MqttUserData = None
    ):
        super(HanMqttClient, self).__init__(client_id=client_id, userdata=user_data)

        self.user_data = user_data
        self.message_handler = MessageHandler(client=self)

        self.connection_start = None

        self.connection_handler = ConnectionHandler(
            client=self, host=host, port=port
        )
        self.publish_handler = PublishHandler(client=self)
        self.subscription_handler = SubscriptionHandler(client=self)

        self.on_message = self.message_handler.handle_message
        self.on_publish = self.publish_handler.handle_publish
        self.on_subscribe = self.subscription_handler.handle_subscribe
        self.on_unsubscribe = self.subscription_handler.handle_unsubscribe
        self.on_connect = self.connection_handler.handle_connect
        self.on_disconnect = self.connection_handler.handle_disconnect

        self.add_topic_blueprint(DEFAULT_TOPIC_BLUEPRINT)

    def subscribe(
        self,
        topic: str,
        qos: int = 0,
        options: Dict[str, Any] = None,
        properties: Dict[str, Any] = None,
    ) -> None:
        if self.is_connected():
            self.subscription_handler.subscribe(
                topic=topic, qos=qos, options=options, properties=properties
            )
        else:
            self.subscription_handler.lazy_subscribe(
                topic=topic, qos=qos, options=options, properties=properties
            )

    def publish(
        self,
        topic: str,
        payload: Dict[str, Any] = None,
        qos: int = 0,
        retain: bool = False,
        properties: Dict = None,
    ) -> MQTTMessageInfo:
        return self.publish_handler.publish(
            topic=topic, payload=payload, qos=qos, retain=retain
        )

    def add_topic_message_handler(self, topic: str, handler: Callable) -> int:
        return self.message_handler.add_topic_message_handler(
            topic=topic, handler=handler
        )

    def remove_topic_message_handler(self, topic: str, handler_id: int) -> None:
        return self.message_handler.remove_topic_message_handler(
            topic=topic, handler_id=handler_id
        )

    def add_topic_publish_handler(self, topic: str, handler: Callable) -> int:
        return self.publish_handler.add_topic_publish_handler(
            topic=topic, handler=handler
        )

    def remove_topic_publish_handler(self, topic: str, handler_id: int) -> None:
        return self.publish_handler.remove_topic_publish_handler(
            topic=topic, handler_id=handler_id
        )

    def add_topic_subscribe_handler(self, topic: str, handler: Callable) -> int:
        return self.subscription_handler.add_topic_subscribe_handler(
            topic=topic, handler=handler
        )

    def remove_topic_subscribe_handler(self, topic: str, handler_id: int) -> None:
        return self.subscription_handler.remove_topic_subscribe_handler(
            topic=topic, handler_id=handler_id
        )

    def add_topic_unsubscribe_handler(self, topic: str, handler: Callable) -> int:
        return self.subscription_handler.add_topic_unsubscribe_handler(
            topic=topic, handler=handler
        )

    def remove_topic_unsubscribe_handler(self, topic: str, handler_id: int) -> None:
        return self.subscription_handler.remove_topic_unsubscribe_handler(
            topic=topic, handler_id=handler_id
        )

    def add_connect_handler(self, handler: Callable) -> int:
        return self.connection_handler.add_connect_handler(handler=handler)

    def remove_connect_handler(self, handler_id: int) -> None:
        return self.connection_handler.remove_connect_handler(handler_id=handler_id)

    def add_disconnect_handler(self, handler: Callable) -> int:
        return self.connection_handler.add_disconnect_handler(handler=handler)

    def remove_disconnect_handler(self, handler_id: int) -> None:
        return self.connection_handler.remove_disconnect_handler(handler_id=handler_id)

    def run(self) -> None:
        LOG.info("Starting MQTT client.")
        self.connection_handler.connect()
        self.subscription_handler.enact_subscriptions()
        self.loop_forever()

    def add_topic_blueprint(self, blueprint: TopicBlueprint, topic_prefix: str = ""):
        for topic in blueprint.topic_action_handlers:
            for handler in blueprint.topic_action_handlers[topic].get("subscribe", []):
                self.add_topic_subscribe_handler(topic=f"{topic_prefix}{topic}", handler=handler)
            for handler in blueprint.topic_action_handlers[topic].get("unsubscribe", []):
                self.add_topic_unsubscribe_handler(topic=f"{topic_prefix}{topic}", handler=handler)
            for handler in blueprint.topic_action_handlers[topic].get("publish", []):
                self.add_topic_publish_handler(topic=f"{topic_prefix}{topic}", handler=handler)
            for handler in blueprint.topic_action_handlers[topic].get("message", []):
                self.add_topic_message_handler(topic=f"{topic_prefix}{topic}", handler=handler)

            self.subscribe(topic=f"{topic_prefix}{topic}")

