import logging
import os

from midge import MidgeMqttClient

from topics.report import REPORT_TOPIC_BLUEPRINT
from topics.meta import META_TOPIC_BLUEPRINT

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_mqtt_client() -> MidgeMqttClient:
    mqtt_client = MidgeMqttClient(
        client_id=os.environ["CLIENT_ID"],
        host=os.environ["BROKER_HOST"],
        port=int(os.environ["BROKER_PORT"]),
        username=os.environ["CLIENT_USER"],
        password=os.environ["CLIENT_PASSWORD"],
        ca_cert="/app/tls/ca/ca.crt",
        client_cert="/app/tls/client/client.crt",
        client_key="/app/tls/client/client.key",
    )

    mqtt_client.enable_logger(LOG)
    mqtt_client.add_topic_blueprint(REPORT_TOPIC_BLUEPRINT, topic_prefix="v0")
    mqtt_client.add_topic_blueprint(META_TOPIC_BLUEPRINT, topic_prefix="v0")

    return mqtt_client


client = create_mqtt_client()
client.run()
