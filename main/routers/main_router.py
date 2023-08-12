from fastapi import APIRouter
from lib.schemas.responses import SUCCESS_RESPONSE_DATA

router = APIRouter()


@router.get("/health")
async def status():
    return SUCCESS_RESPONSE_DATA("OK")