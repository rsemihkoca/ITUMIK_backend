from lib.utils.configs import Configs
import json
import logging
logger = logging.getLogger()  # Retrieve the root logger
def check_mqtt_parameters():
    # check if .env variables are defined
    if Configs.MQTT_USERNAME is None:
        raise Exception("MQTT_USERNAME is not defined!")
    if Configs.MQTT_PASSWORD is None:
        raise Exception("MQTT_PASSWORD is not defined!")
    if Configs.MQTT_TOPIC is None:
        raise Exception("MQTT_TOPIC is not defined!")
    if Configs.MQTT_CLUSTER_URL is None:
        raise Exception("MQTT_CLUSTER_URL is not defined!")
    if Configs.MQTT_PORT is None:
        raise Exception("MQTT_PORT is not defined!")

    return True

def check_topic_is_subscribed(topic_name, subscribed_topics):

    if topic_name not in subscribed_topics:
        logger.error("Topic is not subscribed")
        return False
    return True

def check_message_is_valid(msg_payload):
    try:
        new_keys = json.loads(msg_payload).keys()
    except json.decoder.JSONDecodeError:
        logger.error("Payload is not JSON nor JSON-like")
        return False
    else:
        # check values are non-negative only:
        for key in new_keys:
            if not json.loads(msg_payload)[key] in [0, 1, 2]:
                logger.error("Values are not 0, 1 or 2")
                return False
        return True
