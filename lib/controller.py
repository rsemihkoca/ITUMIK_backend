import json

from lib.database import crud
from lib.utils.mqtt_client import MQTTBrokerClient
from lib.utils.mongo_client import MongoDBClient
from lib.validators import mqtt_validators, mongo_validators
from lib.configs.constants import Constants, DBConstants
from lib.utils.configs import Configs
from pathlib import Path

log_config_path = Path(__file__).resolve().parent / "logging" / "logging_config.json"
floor_config_path = Path(__file__).resolve().parent.parent / "floor-config.json"
desk_config_path = Path(__file__).resolve().parent.parent / "desk-config.json"
class ClientController:

    def __init__(self, logger):
        # self.logger = CustomizeLogger.make_logger(log_config_path)
        self.logger = logger
        self.desk = {Configs.MQTT_TOPIC: {"TL": 0, "TR": 0, "BL": 0, "BR": 0}}
        self.mongo_client = MongoDBClient(self.logger) if mongo_validators.check_mongodb_parameters() else None
        self.mqtt_client = MQTTBrokerClient(self.logger) if mqtt_validators.check_mqtt_parameters() else None
        self.mqtt_client.client.on_message = self.on_message


    #################### MQTT ####################
    def start(self):
        # Listen incoming messages
        self.mqtt_client.start()

    def stop(self):
        try:
            self.mqtt_client.stop()
            self.mongo_client.client.close()
        except Exception as e:
            self.logger.error(e)
            raise e

    def subscribe(self, topics):
        # Subscribe to topics
        self.mqtt_client.subscribe(topics)

    def publish(self, topic, payload):
        # Publish to topics
        self.mqtt_client.publish(topic, payload)

    def on_message(self, client, userdata, msg):
        """Callback when the device receives a message."""
        if not mqtt_validators.check_message_is_valid(msg.payload):
            return
        if not mongo_validators.validate_topic_name(msg.topic):
            return
        if not mqtt_validators.check_topic_is_subscribed(msg.topic, self.mqtt_client.client.subscribed_topics):
            return

        new_values = json.loads(msg.payload)
        existing_keys = "TL TR BL BR".split(" ")

        if not existing_keys == [*new_values.keys()]:
            self.logger.error("Keys are not equal")
            return

        self.desk[Configs.MQTT_TOPIC] = new_values
        self.update_document(DBConstants.TOPIC, msg.topic, new_values)
        self.logger.info(f"Updated {msg.topic} with a received message")

    #################### MONGO ####################
    # def read_document(self, document_field_name, document_field_value):
    #     # UNTESTED
    #     try:
    #         crud.read_document(document_field_name, document_field_value)
    #     except Exception as e:
    #         self.logger.error(e)
    #         raise e

    def update_document(self, document_field_name, document_field_value, update_data):
        try:
            if not document_field_value in self.mongo_client.existing_topics:
                self.logger.error(f"Document with {document_field_name}={document_field_value} does not exist")
                return

            crud.update_document(document_field_name, document_field_value, update_data)
        except Exception as e:
            self.logger.error(e)
            raise e

