from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_utils.tasks import repeat_every
from main.routers import DeviceRouter
import logging


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081"
]


def create_app() -> FastAPI:
    app = FastAPI(title='CustomLogger', debug=False)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.include_router(DeviceRouter.router, prefix="/device", tags=["device"])

    return app