from lib.utils.configs import Configs
import logging
logger = logging.getLogger()  # Retrieve the root logger

def check_mongodb_parameters():
    # check if .env variables are defined
    # if Configs.DB_USERNAME is None:
    #     raise Exception("DB_USERNAME is not defined!")
    # if Configs.DB_PASSWORD is None:
    #     raise Exception("DB_PASSWORD is not defined!")
    if Configs.DB_CONNECTION_STRING is None:
        raise Exception("DB_CONNECTION_STRING is not defined!")
    if Configs.DB_NAME is None:
        raise Exception("DB_NAME is not defined!")
    if Configs.DB_COLLECTION_NAME is None:
        raise Exception("DB_COLLECTION_NAME is not defined!")

    return True

def validate_topic_name(topic_name):
    if topic_name != Configs.MQTT_TOPIC:
        logger.error(f"Topic name {topic_name} is not valid!")
        return False
    return True