
from lib.utils.configs import Configs


def check_mqtt_parameters():
    # check if .env variables are defined
    if not Configs.MQTT_USERNAME:
        raise Exception("MQTT_USERNAME is not defined!")
    if not Configs.MQTT_PASSWORD:
        raise Exception("MQTT_PASSWORD is not defined!")
    if not Configs.MQTT_CLUSTER_URL:
        raise Exception("MQTT_CLUSTER_URL is not defined!")
    if not Configs.MQTT_PORT:
        raise Exception("MQTT_PORT is not defined!")
    if not Configs.MQTT_TOPIC:
        raise Exception("MQTT_TOPIC is not defined!")
    if not Configs.MQTT_CLIENT_ID:
        raise Exception("MQTT_CLIENT_ID is not defined!")

    return True