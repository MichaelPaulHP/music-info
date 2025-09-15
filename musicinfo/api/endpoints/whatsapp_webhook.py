from fastapi import FastAPI, Request, Response
from fastapi import APIRouter
import logging

from musicinfo.core.messaging.whatsapp import process_whatsapp_message

router = APIRouter( )
logger = logging.getLogger(__name__)


@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    # Obtener el cuerpo de la solicitud
    # Handle Webhook Subscriptions
    body = await request.body()
    print('r body: {}'.format(body))

    data = await request.json()
    print('r data: {}'.format(data))

    try:
        # Extraer datos relevantes y procesarlos
        processed_result = await process_whatsapp_message(data, None)
        return {"status": "processed", "result": "ok"}
    except Exception as e:
        logger.error(f"Error processing WhatsApp message: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.get("/webhook")
async def verify_whatsapp_webhook(request: Request):
    # Obtener el parámetro "hub.mode" de la solicitud
    mode = request.query_params.get("hub.mode")

    # Obtener el parámetro "hub.challenge" de la solicitud
    challenge = request.query_params.get("hub.challenge")

    # Verificar si la solicitud es una suscripción
    if mode == "subscribe":
        print(challenge)
        # Devolver el valor del parámetro "hub.challenge" para confirmar la suscripción
        return Response(content=challenge, status_code=200)

    # Si no es una solicitud de suscripción, devolver una respuesta de error
    return {"error": "Invalid request"}
