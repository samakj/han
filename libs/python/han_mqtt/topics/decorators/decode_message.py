import jwt
import logging
from datetime import datetime
from typing import Callable, Optional

from paho.mqtt.client import Client as MQTTClient, MQTTMessage
from han_mqtt.models.UserData import MqttUserData

LOG = logging.getLogger(__name__)


def decode(
    key: str,
    log_on_error: bool = True,
    call_on_error: bool = False,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(client: MQTTClient, user_data: MqttUserData, message: MQTTMessage) -> Optional[Callable]:
            if message.payload:
                client_id = user_data.client_id if user_data is not None else None
                decoded_payload = None

                try:
                    decoded_payload = jwt.decode(message.payload, key)
                except jwt.exceptions.DecodeError:
                    if log_on_error:
                        LOG.error(
                            f"{datetime.utcnow()}: Unable to decode jwt payload sent to '{message.topic}'. "
                            f"client_id: {client_id}."
                        )

                    if not call_on_error:
                        return None

                message.payload = decoded_payload
            return func(client=client, user_data=user_data, message=message)
        return wrapper
    return decorator
