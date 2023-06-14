from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main.routers import main_router
from lib.controller import ClientController

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081"
]


tags_metadata = [
    {
        "name": "Main",
        "description": "Operations with base object.",
    }
    # ,
    # {
    #     "name": "items",
    #     "description": "Manage items. So _fancy_ they have their own docs.",
    #     "externalDocs": {
    #         "description": "Items external docs",
    #         "url": "https://fastapi.tiangolo.com/",
    #     },
    # },
]

def create_app(logger) -> FastAPI:
    app = FastAPI(title='MIK Project', debug=False, version='0.1.0', openapi_tags=tags_metadata)
    app.controller = ClientController(logger)

    app.controller.logger.info("App Started!")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(main_router.router, prefix="/main", tags=["Main"])  # dependencies=[Depends(get_auth)])

    # @app.exception_handler(CustomError)
    # async def custom_error_handler(request: Request, exc: CustomError):
    #     return error_response(message=exc.message, code=exc.code, status_code=exc.status_code)

    return app