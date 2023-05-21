import sys
import http3
import uvicorn

sys.path.append("..")
sys.path.append("../lib/")

from factory import create_app
from dotenv import load_dotenv
load_dotenv(".env")


from lib.utils.configs import Configs
from lib.utils.mqtt_client import MQTTBrokerClient


app = create_app()

client = http3.AsyncClient()
@app.get("/")
async def root():
    app.logger.info("Main API is running now")

    mqtt_broker = MQTTBrokerClient(Configs.MQTT_USERNAME, Configs.MQTT_PASSWORD, Configs.MQTT_CLUSTER_URL, Configs.MQTT_PORT)
    mqtt_broker.subscribe("Kat1/#")
    mqtt_broker.publish("Kat1/Masa1", "Doluluk orani: %50")
    mqtt_broker.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
