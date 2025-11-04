from langchain_core.tools import tool

from musicinfo.core  import messenger


@tool
def send_whatsapp_template(phone_number,template_name, template_components):
    """ Envia un template message to whatsapp
    """
    messenger.send_template(template=template_name,
                            recipient_id=phone_number, lang="es", components=template_components)
    print(f"WHATSAPP: ${template_name}  ${template_components}")
    return "Success"