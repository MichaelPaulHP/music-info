import os

from langchain_core.messages import HumanMessage
import json
from dotenv import load_dotenv
load_dotenv()
from musicinfo.core.messaging.messenger import messenger



def send_message_test(mobile, input_text ):
    # graph = get_graph()
    # messages_input = [HumanMessage(content=input_text)]
    # messages = graph.invoke({"messages": messages_input})
    # last_message = messages["messages"][-1].content
    last_message="HOLAA"
    #messenger.send_message(last_message, mobile)
    components = json.dumps({
        "title":"Hola",
        "info:":"hoooooooooooooooooola"
    })
    components = [
            {
              "type": 'body',
              "parameters": [
                { "type": 'text', "title": 'valor_variable_1' },
                { "type": 'text', "info": 'valor_variable_2' }

              ]
            }
    ]
    components= [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "Título del mensaje",
              "parameter_name":"title"
          },
          {
            "type": "text",
            "text":  input_text,
              "parameter_name":"info"
          }
        ]
      }
    ]
    #messenger.send_message('Hola', '51999766470')
    #messenger.send_template(template="track_info_simple",
    #                        recipient_id="51999766470", lang="es", components= components  )
    #messenger.send_template("hello_world", "51999766470", lang="es", components= components)
    messenger.send_message(input_text,mobile)


def send_typing( message_id ):
    body = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
            "typing_indicator": {
                "type": "text"
            }
    }
    messenger.send_custom_json(body)


#send_message_test("51999766470", "maría magdalena - Sandra")
#send_typing("51999766470" )
