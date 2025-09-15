from langchain_core.tools import tool


@tool
def build_whatsapp_error_template_message(message: str):
    """build a whatsapp template message to send an error """
    print(f"build_error_template ")
    text = f"🛠️{ message}"
    return {
    "template": "track_info_log",
    "components":[
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": text,
                        "parameter_name": "msg"
                    }
                ]
            }
        ]
    }
