from lib.utils.configs import Configs
from lib.utils.mqtt_client import MQTTBrokerClient


class ClientController:
    """
    ClientManager yazılmalı !!!!!!!
    """
    def __init__(self):
        self.mqtt_client = MQTTBrokerClient(Configs.MQTT_CLIENT_ID)

