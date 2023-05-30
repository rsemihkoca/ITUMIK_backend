import sys
import time

import http3
import uvicorn
sys.path.append("..")
sys.path.append("../lib/")
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from factory import create_app
from lib.utils.configs import Configs
from lib.controller import ClientController

# Inıtialize app
app = create_app()

client = http3.AsyncClient()

@app.get("/")
async def root():
    try:

        app.__setattr__("controller", ClientController())
        app.controller.logger.info("App Started!")
        subscription_topics = app.controller.desk_manager.get_subscribes()
        app.controller.mqtt_client.start()
        app.controller.mqtt_client.subscribe(subscription_topics)
        app.controller.mqtt_client.publish("Floor1/Desk1", b'{"Chair1":0, "Chair2":0, "Chair3":0, "Chair4":0}')
        # app.controller.mqtt_client.subscribe(Configs.MQTT_TOPIC)
        # app.controller.mqtt_client.publish(Configs.MQTT_TOPIC, "Doluluk orani: %50")
        # Listen for messages
        # Publish a message

    except Exception as e:
        app.controller.mqtt_client.stop()
        app.controller.logger.error(e)
        raise e
    except KeyboardInterrupt:
        app.controller.mqtt_client.stop()
        app.controller.logger.error("KeyboardInterrupt")
        return
    else:
        return {"message": "Successfully Executed!"}
    finally:
        # Stop listening
        pass
@app.get("/status")
async def status():
    return app.controller.desk_manager.get_status()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
