from langchain_core.tools import tool
from musicinfo.core.messaging.messenger import messenger


@tool
def send_simple_message(message, phone_number):
    """ Envia un mensaje simple a un phone number de whatsapp
    """
    component = [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": message,
            "parameter_name":"msg"
          },
        ]
      }
    ]
    res = messenger.send_template(template='track_info_log',
                            recipient_id=phone_number, lang="es", components=component)
    print(f"WHATSAPP: ${message}  ${component}")
    print(f"WHATSAPP RES: ${res}  ")
    return "Success"