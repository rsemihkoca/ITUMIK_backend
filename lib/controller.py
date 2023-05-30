from lib.utils.configs import Configs
from lib.utils.logger import CustomLogger
from lib.utils.mqtt_client import MQTTBrokerClient
from lib.validators.mqtt_validators import check_mqtt_parameters
from lib.configs.constants import Constants
from lib.configs.desk import DeskManager
from lib.logging.custom_logging import CustomizeLogger
from pathlib import Path

log_config_path = Path(__file__).resolve().parent / "logging" / "logging_config.json"
floor_config_path = Path(__file__).resolve().parent.parent / "floor-config.json"
class ClientController:
    """
    ClientManager yazılmalı !!!!!!!
    """
    def __init__(self):
        # self.logger = CustomLogger(index=Constants.MAIN_CONTROLLER)
        self.logger = CustomizeLogger.make_logger(log_config_path)
        self.desk_manager = DeskManager(floor_config_path)
        self.mqtt_client = MQTTBrokerClient(Configs.MQTT_CLIENT_ID, self.logger, self.desk_manager) if check_mqtt_parameters() else None

