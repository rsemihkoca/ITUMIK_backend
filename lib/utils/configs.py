from lib.utils.helper import get_topic_name

from pydantic import BaseSettings


class Settings(BaseSettings):
    MQTT_USERNAME: str
    MQTT_PASSWORD: str
    MQTT_TOPIC: str = get_topic_name()
    MQTT_CLUSTER_URL: str
    MQTT_PORT: int
    MQTT_CLIENT_ID: str
    MQTT_KEEPALIVE: int
    MQTT_CLEAN_SESSION: bool

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_COLLECTION_NAME: str
    class Config:
        env_file = ".env"


Configs = Settings()
