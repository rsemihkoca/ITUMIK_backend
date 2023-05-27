import sys
import http3
import uvicorn
sys.path.append("..")
sys.path.append("../lib/")
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from factory import create_app
from lib.utils.configs import Configs

# Inıtialize app
app = create_app()

client = http3.AsyncClient()
@app.get("/")
async def root():

    try:

        app.controller.mqtt_client.subscribe(Configs.MQTT_TOPIC)
        app.controller.mqtt_client.publish(Configs.MQTT_TOPIC, "Doluluk orani: %50")
        #TODO: Health check devam et, subscribe ve publish loop dene
        # Listen for messages
        app.controller.mqtt_client.start()
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
        #app.controller.mqtt_client.stop()
        pass



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
