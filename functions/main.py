
from firebase_functions import https_fn
from firebase_admin import initialize_app
from musicinfo.core.messaging.whatsapp import process_whatsapp_message
import asyncio
import logging
import sys

# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
# logging.getLogger().addHandler(handler)
# logging.getLogger().setLevel(logging.INFO)
initialize_app()




@https_fn.on_request()
def webhook(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    original = req.args.get("text")
    logging.info(f"HI ! from webhook with logging.info ")
    print('START REQ')
    print(req)
    print('END REQ')
    challenge = req.args.get("hub.challenge")
    mode = req.args.get("hub.mode")
    print(f"challenge: {challenge}")
    print(f"mode: {mode}")
    if mode == "subscribe":
        return challenge


    elif req.method == 'POST':
        # Lógica para peticiones POST
        # Aquí procesarías los mensajes entrantes de WhatsApp
        request_json = req.get_json(silent=True)
        print(' POST START JSON --------------')
        print(request_json)
        print(' POST END JSON  ----------')
        # Integrar con tu grafo de LangChain/LangGraph
        # ...
        asyncio.run(process_whatsapp_message(request_json, None))


        return {"status": "success", "message": "Procesado correctamente"}

    # Send back a message that we've successfully written the message
    return https_fn.Response(f"Message with ID   added.")
