import sys

import uvicorn
sys.path.append(".")
sys.path.append("..")
sys.path.append("../lib/")
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from lib.utils.configs import Configs
from factory import create_app
from lib.logging.custom_logging import CustomizeLogger
from pathlib import Path

# Inıtialize app
log_config_path = Path(__file__).resolve().parent.parent / "lib" / "logging" / "logging_config.json"
logger, logging_config = CustomizeLogger.make_logger(log_config_path)
app = create_app(logger)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to this fantastic app!"}
@app.on_event("shutdown")
def shutdown_db_client():
    app.controller.stop()


if __name__ == "__main__":
    app.controller.start()
    # Subscribe to topics
    app.controller.subscribe(Configs.MQTT_TOPIC)
    # Publish to topics
    app.controller.publish(Configs.MQTT_TOPIC, b'{"TL": 0, "TR": 0, "BL": 1, "BR": 2}')

    uvicorn.run(app, host="0.0.0.0", port=8008)
