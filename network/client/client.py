import logging
import os
import re
import uuid

from han_secure_mqtt import HanMqttClient, HanMqttUserData

from topics.report import REPORT_TOPIC_BLUEPRINT

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_mqtt_client() -> HanMqttClient:
    mqtt_client = HanMqttClient(
        client_id="node_controller",
        host=os.environ["BROKER_HOST"],
        port=int(os.environ["BROKER_PORT"]),
        user_data=HanMqttUserData(
            client_id=':'.join(re.findall('..', '%012x' % uuid.getnode())),
            username="client",
            password=os.environ["CLIENT_PASSWORD"],
        ),
        tls_cert="/app/tls/client/client.crt",
    )

    mqtt_client.enable_logger(LOG)
    mqtt_client.add_topic_blueprint(REPORT_TOPIC_BLUEPRINT, topic_prefix="/v0")

    return mqtt_client


client = create_mqtt_client()
client.run()
