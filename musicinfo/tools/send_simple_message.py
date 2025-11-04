from langchain_core.tools import tool
from musicinfo.core import messenger


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
    res = messenger.send_message(message,phone_number)
    print(f"WHATSAPP: ${message}  ${component}")
    print(f"WHATSAPP RES: ${res}  ")
    return "Success"