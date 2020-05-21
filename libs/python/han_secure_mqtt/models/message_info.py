from dataclasses import dataclass

from paho.mqtt.client import MQTTMessageInfo


@dataclass
class HanMqttMessageInfo(MQTTMessageInfo):
    pass
