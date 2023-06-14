from fastapi import APIRouter, Depends
from starlette.requests import Request
from lib.schemas.responses import SUCCESS_RESPONSE_DATA
# from dependencies import get_current_user

# from lib.utils.responses import success_data_response, handle_exception
# from typing import Optional
# from lib.utils.constants import Constants
# from lib.data_types.base import User
router = APIRouter()


@router.get("/status")
async def status(request: Request):
    status = request.app.controller.desk_manager.get_status()
    return SUCCESS_RESPONSE_DATA(status)