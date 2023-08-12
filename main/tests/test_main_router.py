import sys
import unittest, pytest

sys.path.append(".")
sys.path.append("../main")
sys.path.append("../../lib/")
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


from fastapi.testclient import TestClient
from main.factory import create_app
from lib.configs.data import TestPayload
from lib.utils.configs import Configs
from lib.logging.custom_logging import CustomizeLogger
from pathlib import Path
# Inıtialize app
log_config_path = Path(__file__).resolve().parent.parent.parent / "lib" / "logging" / "logging_config.json"
logger, logging_config = CustomizeLogger.make_logger(log_config_path)
app = create_app(logger)
client = TestClient(app)
class SubscribeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global app
        # SETUP
        app.controller.start()


    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def test_subscribe(self):

        """
        @app.controller.subscribe()
        """
        subscription_topics = [Configs.MQTT_TOPIC]
        app.controller.subscribe()
        subscribed_topics = app.controller.mqtt_client.client.subscribed_topics
        self.assertEqual(subscribed_topics, subscription_topics)
    # def test_get_status(self):
    #     """
    #     test @app.get("/main/status")
    #     """
    #
    #     response = client.get("/main/status")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), TestPayload.test_get_status)



