import logging
import os
import re
import uuid

from han_secure_mqtt import HanMqttClient

from topics.report import REPORT_TOPIC_BLUEPRINT

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_mqtt_client() -> HanMqttClient:
    mqtt_client = HanMqttClient(
        client_id=":".join(re.findall('..', '%012x' % uuid.getnode())),
        host=os.environ["BROKER_HOST"],
        port=int(os.environ["BROKER_PORT"]),
        username="client",
        password=os.environ["CLIENT_PASSWORD"],
        ca_cert="/app/tls/ca/ca.crt",
        client_cert="/app/tls/client/client.crt",
        client_key="/app/tls/client/client.key",
    )

    mqtt_client.enable_logger(LOG)
    mqtt_client.add_topic_blueprint(REPORT_TOPIC_BLUEPRINT, topic_prefix="/v0")

    return mqtt_client


client = create_mqtt_client()
client.run()
