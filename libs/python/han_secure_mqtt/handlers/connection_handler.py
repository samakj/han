import logging
from typing import Any, Callable, Dict, List, Optional

from han_secure_mqtt.models.response_code import ResponseCode
from han_secure_mqtt.models.reason_codes import ReasonCodesMap
from han_secure_mqtt.models.error_codes import ErrorCodesMaps
from han_secure_mqtt.models.user_data import HanMqttUserData
from paho.mqtt.client import Client as MQTTClient

LOG = logging.getLogger(__name__)


class ConnectionHandler:
    def __init__(self, client, host: str, port: int, keep_alive: int = 60):
        self.client = client
        self.host = host
        self.port = port
        self.keep_alive = keep_alive
        self._connection_handlers: Dict[int, Callable] = {}
        self._disconnection_handlers: Dict[int, Callable] = {}

    def connect(self) -> ResponseCode:
        LOG.info(f"Connecting to broker at {self.host}:{self.port}")
        error_code = self.client.connect(host=self.host, port=self.port, keepalive=self.keep_alive)
        return ErrorCodesMaps[error_code]

    def add_connect_handler(self, handler: Callable) -> int:
        handler_id = len(self._connection_handlers)
        self._connection_handlers[handler_id] = handler

        return handler_id

    def get_connect_handler(self, handler_id: int) -> Optional[Callable]:
        return self._connection_handlers.get(handler_id, None)

    def get_connect_handlers(self) -> List[Callable]:
        return list(self._connection_handlers.values())

    def remove_connect_handler(self, handler_id: int) -> None:
        if handler_id in self._connection_handlers:
            del self._connection_handlers[handler_id]

    def handle_connect(
        self,
        _: MQTTClient,
        userdata: HanMqttUserData,
        flags: Dict[str, Any],
        rc: int,
        properties: Dict[str, Any] = None,
    ) -> None:
        userdata = userdata or HanMqttUserData()
        for handler in self.get_connect_handlers():
            try:
                handler(
                    client=self.client,
                    user_data=userdata,
                    flags=flags,
                    reason_code=ReasonCodesMap[rc],
                    properties=properties,
                )
            except Exception as Error:
                LOG.exception(Error)

    def disconnect(
        self, reason_code: Optional[int] = None, properties: Dict[str, Any] = None
    ) -> None:
        error_code = self.client.disconnect(reasoncode=reason_code, properties=properties)
        return ErrorCodesMaps[error_code]

    def add_disconnect_handler(self, handler: Callable) -> int:
        handler_id = len(self._disconnection_handlers)
        self._disconnection_handlers[handler_id] = handler

        return handler_id

    def get_disconnect_handler(self, handler_id: int) -> Optional[Callable]:
        return self._disconnection_handlers.get(handler_id, None)

    def get_disconnect_handlers(self) -> List[Callable]:
        return list(self._disconnection_handlers.values())

    def remove_disconnect_handler(self, handler_id: int) -> None:
        if handler_id in self._disconnection_handlers:
            del self._disconnection_handlers[handler_id]

    def handle_disconnect(
        self,
        _: MQTTClient,
        userdata: HanMqttUserData,
        rc: int,
        properties: Dict[str, Any] = None,
    ) -> None:
        userdata = userdata or HanMqttUserData()
        for handler in self.get_disconnect_handlers():
            try:
                handler(client=self.client, userdata=userdata, reason_code=ReasonCodesMap[rc], properties=properties)
            except Exception as Error:
                LOG.exception(Error)
