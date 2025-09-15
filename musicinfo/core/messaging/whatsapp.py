from heyoo import WhatsApp
import os
import logging

from langchain_core.messages import HumanMessage

from musicinfo.workflows import full_tools_workflow

logger = logging.getLogger(__name__)

messenger = WhatsApp(os.getenv('WHATSAPP_TOKEN'), phone_number_id=os.getenv('WHATSAPP_ID_PHONE_NUMBER'))


def validate_whatsapp_text(message, max_chars=4000):
    if len(message) > max_chars:
        raise ValueError(
            f"El texto excede el límite de {max_chars} caracteres. "
            f"Longitud actual: {len(message)} caracteres."
        )
    return message

def build_whatsapp_message_component(title, info):
    return [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": title,
              "parameter_name":"title"
          },
          {
            "type": "text",
            "text": info,
              "parameter_name":"info"
          }
        ]
      }
    ]

loaded = {}

async def process_whatsapp_message(data, llm_service:None):
    print(f'dict size: {len(loaded) }')


    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    changed_field.
    if changed_field == "messages":
        message_id = messenger.get_message_id(data)
        if message_id in loaded:
            return
        else:
            loaded[message_id] = True

        new_message = messenger.get_mobile(data)
        if message_id and new_message:

            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info(f"{mobile} sent {message} ")

                try:
                    # Validar el texto
                    text_validated = validate_whatsapp_text(message, max_chars=500)
                    print("AGENT TASK")
                    graph = full_tools_workflow.graph
                    messages_input = [HumanMessage(content=f"{text_validated}. phone number: {mobile}")]
                    messages = graph.invoke({"messages": messages_input})

                except ValueError as e:
                    next_message = "💥"
                    messenger.send_message(next_message, mobile)
            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                interactive_type = message_response.get("type")
                message_id = message_response[interactive_type]["id"]
                message_text = message_response[interactive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)

            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_caption = image["caption"]
                print(f"AGENT TASK ${image_caption}")
                graph = full_tools_workflow.graph
                messages_input = [HumanMessage(content=f"{image_caption}. phone number: {mobile}")]
                messages = graph.invoke({"messages": messages_input})

            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                # video_url = messenger.query_media_url(video_id)
                # video_filename = messenger.download_media(video_url, mime_type)
                # print(f"{mobile} sent video {video_filename}")
                # logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                #audio_filename = messenger.download_media(audio_url, mime_type)
                #print(f"{mobile} sent audio {audio_filename}")
                #logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "document":
                file = messenger.get_document(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                #file_filename = messenger.download_media(file_url, mime_type)
                #print(f"{mobile} sent file {file_filename}")
                #logging.info(f"{mobile} sent file {file_filename}")
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")