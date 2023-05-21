from fastapi import FastAPI
from lib.controller import ClientController
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_utils.tasks import repeat_every
from routers import DeviceRouter
import logging


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081"
]


def create_app():
    app = FastAPI()
    app.logger = logging.getLogger()
    app.logger.info("Main API is running now")
    app.controller = ClientController()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.include_router(DeviceRouter.router, prefix="/device", tags=["device"])

    # @app.on_event("startup")
    # # @repeat_every(seconds=600)
    # async def check_smth() -> None:
    #     app.controller.X()

    return app