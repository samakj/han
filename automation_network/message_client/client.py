import logging
import os

from han_mqtt import HanMqttClient

from topics.meta import META_TOPIC_BLUEPRINT
from topics.report import REPORT_TOPIC_BLUEPRINT

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_mqtt_client() -> HanMqttClient:
    client = HanMqttClient(
        client_id="node_controller",
        host=os.environ["BROKER_HOST"],
        port=int(os.environ["BROKER_PORT"]),
    )

    client.enable_logger(LOG)

    client.add_topic_blueprint(META_TOPIC_BLUEPRINT, topic_prefix="/v0")
    client.add_topic_blueprint(REPORT_TOPIC_BLUEPRINT, topic_prefix="/v0")

    return client


client = create_mqtt_client()
client.run()
