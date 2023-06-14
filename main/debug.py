import sys

import uvicorn
sys.path.append(".")
sys.path.append("..")
sys.path.append("../lib/")
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from factory import create_app
from lib.controller import ClientController
from lib.logging.custom_logging import CustomizeLogger
from pathlib import Path

# Inıtialize app
log_config_path = Path(__file__).resolve().parent.parent / "lib" / "logging" / "logging_config.json"
logger, logging_config = CustomizeLogger.make_logger(log_config_path)
app = create_app(logger)

@app.get("/", tags=["Root"])
async def root():
    try:
        # SETUP
        subscription_topics = app.controller.desk_manager.get_subscribes()

        # Listen incoming messages
        app.controller.start()

        # Subscribe to topics
        app.controller.subscribe(subscription_topics)

        # Publish to topics
        app.controller.publish("Floor1/Desk1", b'{"Chair1":true, "Chair2":true, "Chair3":false, "Chair4":true}')

    except Exception as e:
        # app.controller.stop()
        app.controller.logger.error(e)
        # raise e
    except KeyboardInterrupt:
        # app.controller.stop()
        app.controller.logger.error("KeyboardInterrupt")
        return
    else:
        return {"message": "Successfully Executed!"}

@app.on_event("shutdown")
def shutdown_db_client():
    app.controller.stop()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
