from lib.utils.configs import Configs
from lib.utils.logger import CustomLogger
from lib.utils.mqtt_client import MQTTBrokerClient
from lib.validators.mqtt_validators import check_mqtt_parameters
from lib.configs.constants import Constants

class ClientController:
    """
    ClientManager yazılmalı !!!!!!!
    """
    def __init__(self):
        self.logger = CustomLogger(index=Constants.MAIN_CONTROLLER)
        self.mqtt_client = MQTTBrokerClient(Configs.MQTT_CLIENT_ID, self.logger) if check_mqtt_parameters() else None

