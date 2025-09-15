import os
from heyoo import WhatsApp
from dotenv import load_dotenv
load_dotenv()

messenger = WhatsApp(os.getenv('WHATSAPP_TOKEN'), phone_number_id=os.getenv('WHATSAPP_ID_PHONE_NUMBER'))
