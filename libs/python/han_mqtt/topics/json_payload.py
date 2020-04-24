import json
import logging
from datetime import datetime
from typing import Callable, Optional

from paho.mqtt.client import Client as MQTTClient, MQTTMessage
from han_mqtt.models.UserData import MqttUserData

LOG = logging.getLogger(__name__)


def json_payload(call_on_error: bool = False, log_on_error: bool = False) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(client: MQTTClient, user_data: MqttUserData, message: MQTTMessage) -> Optional[Callable]:
            if message.payload:
                client_id = user_data.client_id if user_data is not None else None
                loaded_json = None

                try:
                    loaded_json = json.loads(message.payload)
                except json.JSONDecodeError:
                    if log_on_error:
                        LOG.error(
                            f"{datetime.utcnow()}: Malformed payload sent to '{message.topic}'. "
                            f"client_id: {client_id}."
                        )

                    if not call_on_error:
                        return

                message.payload = loaded_json
            return func(client=client, user_data=user_data, message=message)
        return wrapper
    return decorator
