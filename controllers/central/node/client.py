import os

from han_mqtt import HanMqttClient


def create_mqtt_client() -> HanMqttClient:
    client = HanMqttClient(
        client_id="node_controller",
        host=os.environ["BROKER_HOST"],
        port=int(os.environ["BROKER_PORT"]),
    )

    return client


client = create_mqtt_client()
client.run()
