import logging
import os
from uuid import getnode

from han_secure_mqtt import HanMqttClient, HanMqttUserData

from topics.report import REPORT_TOPIC_BLUEPRINT

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_mqtt_client() -> HanMqttClient:
    mac_address = hex(getnode())

    mqtt_client = HanMqttClient(
        client_id="node_controller",
        host=os.environ["BROKER_HOST"],
        port=int(os.environ["BROKER_PORT"]),
        user_data=HanMqttUserData(
            client_id=(
                f"{mac_address[2]}{mac_address[3]}:"
                f"{mac_address[4]}{mac_address[5]}:"
                f"{mac_address[6]}{mac_address[7]}:"
                f"{mac_address[8]}{mac_address[9]}:"
                f"{mac_address[10]}{mac_address[11]}:"
                f"{mac_address[12]}{mac_address[13]}"
            ),
            username="client",
            password=os.environ["CLIENT_PASSWORD"],
        ),
        tls_cert="/app/tls/client.crt",
    )

    mqtt_client.enable_logger(LOG)
    mqtt_client.add_topic_blueprint(REPORT_TOPIC_BLUEPRINT, topic_prefix="/v0")

    return mqtt_client


client = create_mqtt_client()
client.run()
