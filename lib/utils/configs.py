from lib.utils.helper import get_topic_name, str_to_bool
from pydantic import BaseSettings, Field
import logging
import os

logger = logging.getLogger()  # Retrieve the root logger

class Settings(BaseSettings):
    MQTT_USERNAME: str = Field(default=os.getenv("MQTT_USERNAME").strip())
    MQTT_PASSWORD: str = Field(default=os.getenv("MQTT_PASSWORD").strip())
    MQTT_TOPIC: str = Field(default_factory=get_topic_name)  # from desk-config.json
    MQTT_CLUSTER_URL: str = Field(default=os.getenv("MQTT_CLUSTER_URL").strip())
    MQTT_PORT: int = Field(default=int(os.getenv("MQTT_PORT").strip()))
    MQTT_CLIENT_ID: str = Field(default=os.getenv("MQTT_CLIENT_ID").strip())
    MQTT_KEEPALIVE: int = Field(default=int(os.getenv("MQTT_KEEPALIVE").strip()))
    MQTT_CLEAN_SESSION: bool = Field(default=bool(os.getenv("MQTT_CLEAN_SESSION").strip()))

    DB_USERNAME: str = Field(default=os.getenv("DB_USERNAME").strip())
    DB_PASSWORD: str = Field(default=os.getenv("DB_PASSWORD").strip())
    DB_NAME: str = Field(default=os.getenv("DB_NAME").strip())
    DB_COLLECTION_NAME: str = Field(default=os.getenv("DB_COLLECTION_NAME").strip())

    # MongoDB connection string
    @property
    def DB_CONNECTION_STRING(self) -> str:
        return f"mongodb+srv://{self.DB_USERNAME}:{self.DB_PASSWORD}@clustermik.y0qcdbs.mongodb.net/"

    @DB_CONNECTION_STRING.setter
    def DB_CONNECTION_STRING(cls, value):
        logger.error("DB_CONNECTION_STRING is a read-only property and cannot be modified.")

# Initialize the Configs
Configs = Settings()
