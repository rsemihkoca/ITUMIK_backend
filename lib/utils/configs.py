from lib.utils.helper import get_topic_name

from pydantic import BaseSettings, Field
import logging
logger = logging.getLogger()  # Retrieve the root logger
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

    # MongoDB connection string
    @property
    def DB_CONNECTION_STRING(self) -> str:
        return f"mongodb+srv://{self.DB_USERNAME}:{self.DB_PASSWORD}@clustermik.y0qcdbs.mongodb.net/"


    @DB_CONNECTION_STRING.setter
    def DB_CONNECTION_STRING(self, value):
        logger.error("DB_CONNECTION_STRING is a read-only property and cannot be modified.")


Configs = Settings()
