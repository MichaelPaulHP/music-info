import os

from heyoo import WhatsApp
from langchain_core.messages import HumanMessage
import json
from musicinfo.workflows import get_graph
from dotenv import load_dotenv
load_dotenv()

messenger = WhatsApp(os.getenv('WHATSAPP_TOKEN'), phone_number_id=os.getenv('WHATSAPP_ID_PHONE_NUMBER'))


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
    messenger.send_template(template="track_info_simple",
                            recipient_id="51999766470", lang="es", components= components  )
    #messenger.send_template("hello_world", "51999766470", lang="es", components= components)



#send_message_test("51999766470", "maría magdalena - Sandra")
