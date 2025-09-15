import json

from dotenv import load_dotenv
#from langchain_core.messages import HumanMessage

#from musicinfo.tools import format_json, send_simple_message
#from musicinfo.core.messaging.whatsapp_test import send_message_test
#from musicinfo.workflows import full_tools_workflow

load_dotenv()
# import logging
# import sys
# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
# logging.getLogger().addHandler(handler)
# logging.getLogger().setLevel(logging.INFO)

def main():
    # message_tidal = 'Escucha Original Sin en tu servicio de streaming https://tidal.com/track/7935349?u'
    # message_spotify = 'https://open.spotify.com/track/4myFsmx2v6znDOJfn3IkbD?si=zT-JPhNIRZSLXbMQ7JSCLA'
    message_user = 'maría magdalena - Sandra'
    m_json = {
        "metadata": {
            "artista": "The Monkees",
            "cancion": "I'm a Believer"
        },
        "descripcion_general": "La canción 'I'm a Believer', interpretada por The Monkees, es un himno pop sobre el amor y los giros inesperados que nos hacen pasar del escepticismo al fervor apasionado.",
        "historia": "Lanzada en 1966, 'I'm a Believer' fue escrita por Neil Diamond. En medio de la explosión del rock de los años 60, The Monkees, una banda creada para un programa de televisión, capturó la atención del público con su carismático sonido pop. La canción rápidamente alcanzó el número uno en las listas de Billboard, y más tarde tuvo una resurgencia en popularidad cuando Smash Mouth la versionó para la película 'Shrek' en el 2000.",
        "analisis_letra": "La letra cuenta la historia de alguien que inicia escéptico sobre el amor, descartándolo como algo real, hasta que una experiencia personal le cambia la perspectiva. El tema principal gira en torno al poder transformador del amor y la capacidad de hacer que incluso los escépticos más duros se conviertan en 'creyentes'.",
        "frases_destacadas": [
            "Then I saw her face, now I'm a believer (Entonces vi su rostro, y ahora soy un creyente)",
            "Not a trace of doubt in my mind (Ni un rastro de duda en mi mente)"
        ],
        "curiosidades": [
            "Fue la canción más vendida de 1967 en EE.UU.",
            "Neil Diamond grabó su propia versión antes del lanzamiento de The Monkees.",
            "El grupo The Monkees fue creado inicialmente para una serie de televisión del mismo nombre."
        ],
        "canciones_similares": [
            "The Beatles - She Loves You",
            "The Turtles - Happy Together",
            "Herman's Hermits - I'm into Something Good",
            "The Beach Boys - Wouldn't It Be Nice",
            "Gerry and the Pacemakers - How Do You Do It?"
        ],
        "generos": [
            "Pop rock"
        ],
        "generos_relacionados": [
            "Rock and roll",
            "Bubblegum pop"
        ],
        "otros": "La canción, con su pegajosa melodía y tema optimista, ayudó a cimentar la reputación de The Monkees como una de las bandas más queridas de los años 60, dejando una marca indeleble en la cultura pop estadounidense."
    }

    #graph = full_tools_workflow.graph
    mobile="51999766470"
    # messages_input = [HumanMessage(content=f"{message_user}. phone number: {mobile}")]
    # messages = graph.invoke({"messages": messages_input})
    #send_simple_message("asdasdas",mobile)
    #print(messages)


    #send_message_test("51999766470", text)

    pass


if __name__ == '__main__':
    main()
