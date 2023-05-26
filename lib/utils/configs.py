import os


class Configs:
    # get defined .env variables

    # MQTT
    MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
    MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
    MQTT_CLUSTER_URL = os.environ.get("MQTT_CLUSTER_URL")
    MQTT_PORT = int(os.environ.get("MQTT_PORT"))
    MQTT_TOPIC = os.environ.get("MQTT_TOPIC")
    MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID")


