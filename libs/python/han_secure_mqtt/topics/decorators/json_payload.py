import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from paho.mqtt.client import Client as MQTTClient, MQTTMessage

LOG = logging.getLogger(__name__)


def json_payload(call_on_error: bool = False, log_on_error: bool = True) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(
            client: MQTTClient,
            message: MQTTMessage,
            user_data: Optional[Dict[str, Any]] = None
        ) -> Optional[Callable]:
            if message.payload:
                loaded_json = None

                try:
                    loaded_json = json.loads(message.payload)
                except json.JSONDecodeError:
                    if log_on_error:
                        LOG.error(f"{datetime.utcnow()}: Malformed payload sent to '{message.topic}'.")

                    if not call_on_error:
                        return

                message.payload = loaded_json
            return func(client=client, user_data=user_data, message=message)
        return wrapper
    return decorator
