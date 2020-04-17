import jwt
import logging
from datetime import datetime
from typing import Callable, Optional

from paho.mqtt.client import Client as MQTTClient, MQTTMessage
from han_mqtt.models.UserData import MqttUserData

LOG = logging.getLogger(__name__)
DEFAULT_EXPIRY_TIME = 1


def decode(key: str, payload_expiry: int = DEFAULT_EXPIRY_TIME) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(client: MQTTClient, user_data: MqttUserData, message: MQTTMessage) -> Optional[Callable]:
            if message.payload:
                client_id = user_data.client_id if user_data is not None else None

                try:
                    decoded_payload = jwt.decode(message.payload, key)
                except jwt.exceptions.DecodeError:
                    LOG.error(
                        f"{datetime.utcnow()}: Malformed payload sent to '{message.topic}'. "
                        f"client_id: {client_id}."
                    )
                    return

                if datetime.utcnow().timestamp() - decoded_payload.get("timestamp", 0) > payload_expiry:
                    LOG.error(
                        f"{datetime.utcnow()}: Expired payload sent to '{message.topic}'. "
                        f"client_id: {client_id}."
                    )
                    return
                if decoded_payload.get("node_id", None) != user_data.client_id:
                    LOG.error(
                        f"{datetime.utcnow()}: Invalid payload, bad id, sent to '{message.topic}'. "
                        f"client_id: {client_id}."
                    )
                    return

                message.payload = decoded_payload
            return func(client=client, user_data=user_data, message=message)
        return wrapper
    return decorator
