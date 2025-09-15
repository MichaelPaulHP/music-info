from fastapi import APIRouter
from .endpoints import whatsapp_webhook

api_router = APIRouter()
api_router.include_router(whatsapp_webhook.router, prefix="/whatsapp", tags=["Whatsapp Webhook" ])