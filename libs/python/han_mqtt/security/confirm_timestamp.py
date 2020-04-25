import logging
from datetime import datetime
from typing import Callable, Optional

from paho.mqtt.client import Client as MQTTClient, MQTTMessage
from han_mqtt.models.UserData import MqttUserData

LOG = logging.getLogger(__name__)
DEFAULT_EXPIRY_TIME = 1


def confirm_timestamp(
    payload_expiry: int = DEFAULT_EXPIRY_TIME,
    log_on_error: bool = True,
    call_on_error: bool = False,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(client: MQTTClient, user_data: MqttUserData, message: MQTTMessage) -> Optional[Callable]:
            is_valid = False

            if message.payload:
                client_id = user_data.client_id if user_data is not None else None

                if datetime.utcnow().timestamp() - message.payload.get("timestamp", 0) > payload_expiry:
                    if log_on_error:
                        LOG.error(
                            f"{datetime.utcnow()}: Expired payload sent to '{message.topic}'. "
                            f"client_id: {client_id}."
                        )
                else:
                    is_valid = True

            if not is_valid:
                if call_on_error:
                    message.payload = None
                else:
                    return None

            return func(client=client, user_data=user_data, message=message)
        return wrapper
    return decorator
