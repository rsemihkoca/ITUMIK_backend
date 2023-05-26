import sys
import http3
import uvicorn
sys.path.append("..")
sys.path.append("../lib/")
from dotenv import load_dotenv
load_dotenv(".env")

from factory import create_app
from lib.utils.configs import Configs
from validators import mqtt_validators

# Inıtialize app
app = create_app()

client = http3.AsyncClient()
@app.get("/")
async def root():
    app.logger.info("Main API is running now")

    try:
        mqtt_validators.check_mqtt_parameters()
        app.controller.mqtt_client.subscribe(Configs.MQTT_TOPIC)
        # Listen for messages
        app.controller.mqtt_client.start()
        # Publish a message
        app.controller.mqtt_client.publish(Configs.MQTT_TOPIC, "Doluluk orani: %50")
    except Exception as e:
        app.controller.mqtt_client.stop()
        raise e
    else:
        return {"message": "Successfully Executed!"}
    finally:
        # Stop listening
        app.controller.mqtt_client.stop()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
