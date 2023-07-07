from lib.utils.helper import get_topic_name

from pydantic_settings import BaseSettings, Field
import logging
logger = logging.getLogger()  # Retrieve the root logger
class Settings(BaseSettings):
    MQTT_USERNAME: str = Field(...)
    MQTT_PASSWORD: str = Field(...)
    MQTT_TOPIC: str = get_topic_name()  # from desk-config.json
    MQTT_CLUSTER_URL: str = Field(...)
    MQTT_PORT: int = Field(...)
    MQTT_CLIENT_ID: str = Field(...)
    MQTT_KEEPALIVE: int = Field(...)
    MQTT_CLEAN_SESSION: bool = Field(...)

    DB_USERNAME: str = Field(...)
    DB_PASSWORD: str = Field(...)
    DB_NAME: str = Field(...)
    DB_COLLECTION_NAME: str = Field(...)

    class Config:
        env_file = "../.env"

    # MongoDB connection string
    @property
    def DB_CONNECTION_STRING(self) -> str:
        return f"mongodb+srv://{self.DB_USERNAME}:{self.DB_PASSWORD}@clustermik.y0qcdbs.mongodb.net/"


    @DB_CONNECTION_STRING.setter
    def DB_CONNECTION_STRING(cls, value):
        logger.error("DB_CONNECTION_STRING is a read-only property and cannot be modified.")


Configs = Settings()
