import sys
import unittest
sys.path.append("../..")
sys.path.append("../../lib/")
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


import http3



from factory import create_app
from lib.controller import ClientController

app = create_app()

client = http3.AsyncClient()

class SubscribeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global app
        # SETUP
        app.controller = ClientController()
        app.controller.start()


    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def test_get_status(self):

        self.assertEqual(True, True)