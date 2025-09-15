from typing import List, TypedDict, Literal

from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, create_react_agent
from langgraph.prebuilt import ToolNode
from langgraph.types import Command

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")


def main_agent():
    msg = """
    Eres un Agente que trabaja con varios agentes.
    El trabajo en enviar por whatsapp la historia de una cancion.
    Los agentes te van ayudar a resolver eso.
    por cada tarea que hagas envia un mensaje simple por whatsapp
    """
    sys_msg = SystemMessage(content=msg)

    llm = ChatOpenAI(model="gpt-4o")
    return {"sys_msg":sys_msg, "llm":llm}


def whatsapp_agent():
    def send_simple_message(message, phone_number):
        """ Envia un mensaje simple a un phone number de whatsapp
        """
        print(f"WHATSAPP: ${message} ")
        return "Success"

    def send_template(template_name, template_components):
        """ Envia un mensaje simple a un phone number de whatsapp
        """
        print(f"WHATSAPP: ${template_name}  ${template_components}")
        return "Success"

    msg = """
    Eres un Agente que interactua con whatsapp.
    tu reponsabilidad es enviar mensajes simples como mensajes template 
    """
    sys_msg = SystemMessage(content=msg)

    llm = ChatOpenAI(model="gpt-4o")
    tools = [send_simple_message, send_template]
    llm_with_tools = llm.bind_tools(tools)
    return {"sys_msg": sys_msg, "llm": llm_with_tools,"tools":tools}


def track_history_agent():
    def get_track_basic_info(song_raw):
        """Extract basic song info (name and artist) from text."""
        print(f"Getting basic info ${song_raw} ....")
        return """json
        {
            "artist": "The Monkees",
            "song":"I'm a Believer"
        }"""

    def get_song_history(artists: str, song: str):
        """get song history from song name and artist name."""
        print(f"Getting song history ${artists} ${song} ")
        return '''json
       {
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
        '''

    msg = """
    Eres un Agente que busca la historia de una cancion.
    necesitas informacion basica de la cancion: artista y cancion, para obtener la historia.
     
    """
    sys_msg = SystemMessage(content=msg)

    llm = ChatOpenAI(model="gpt-4o")
    tools = [get_track_basic_info, get_song_history]
    llm_with_tools = llm.bind_tools(tools)
    return {"sys_msg": sys_msg, "llm": llm_with_tools, "tools": tools}


def whatsapp_presentation_agent():
    def build_error_template(message: str):
        """ template de whatsapp de un error """
        print(f"build_error_template ")
        return f"""json
        {
        "template": "The Monkees",
        "components":[{message}]
        }
        """

    def build_history_template(texts: list[str]):
         """ template de whatsapp de una historia de una cancion """
         print(f"build_history_template ")
         return f"""json
         {
            "template": "The Monkees",
            "components":[{texts}]
         }"""

    def beautify_texts(texts: List[str]):
        """ Convierte cada texto en un texto mas facil de leer con emojis
        """
        print(f"beautify_texts  ")
        return [
            'Hola 👍'
            'mucho gusto 🥳',
            'End 🫵'
        ]

    msg = """
    Eres un Agente que interactua con whatsapp.
    tu reponsabilidad es enviar mensajes simples como mensajes template 
    """
    sys_msg = SystemMessage(content=msg)

    llm = ChatOpenAI(model="gpt-4o")
    tools = [beautify_texts, build_history_template, build_error_template]
    llm_with_tools = llm.bind_tools(tools)
    return {"sys_msg": sys_msg, "llm": llm_with_tools, "tools":tools}


main_agent = main_agent()
whatsapp_agent = whatsapp_agent()
track_history_agent = track_history_agent()
whatsapp_presentation_agent = whatsapp_presentation_agent()


def main_agent_node(state: MessagesState):
    sys_msg = main_agent["sys_msg"]
    return {"messages": [main_agent["llm"].invoke([sys_msg] + state["messages"])]}


def whatsapp_agent_node(state: MessagesState):
    sys_msg = whatsapp_agent["sys_msg"]
    return {"messages": [whatsapp_agent["llm"].invoke([sys_msg] + state["messages"])]}


def track_history_agent_node(state: MessagesState):
    sys_msg = track_history_agent["sys_msg"]
    return {"messages": [track_history_agent["llm"].invoke([sys_msg] + state["messages"])]}

def whatsapp_presentation_agent_node(state: MessagesState):
    sys_msg = whatsapp_presentation_agent["sys_msg"]
    return {"messages": [whatsapp_presentation_agent["llm"].invoke([sys_msg] + state["messages"])]}

# Graph
builder = StateGraph(MessagesState)


members = ["whatsapp","whatsapp_presentation_agent", "track_history"]
# Our team supervisor is an LLM node. It just picks the next agent to process
# and decides when the work is completed
options = members + ["FINISH"]

system_prompt = (
    f"""Eres un supervisor encargado de manejar la conversacion entre 
    los siguientes agentes: {members}. 
    Responde con el agente que debe hacer el siguiente trabajo. Each worker will perform a 
    Cada agente va responder con su resultado y status. 
    When finished, respond with FINISH. 
    El  objetivo general es enviar por whatsapp la historia de una cancion de manera amigable. 
    Notificar siempre al usuario de las tareas que estas haciendo
    RESPONSABILIDAD DE LOS AGENTES
    - whatsapp: enviar mensaje al usuario. 
    - whatsapp_presentation_agent: todo lo necesario para whatsapp como templates, y mensajes amigables.
    - track_history: obtener historia de una cancion 
    """
)


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]
llm = ChatOpenAI(model="gpt-4o")
def supervisor_node(state: MessagesState) -> Command[Literal[*members, "__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})
# main
builder.add_node("main", supervisor_node)

# tools = []
# supervisor = create_react_agent(main_agent["llm"], tools)
#
# TRACK_HISTORY
builder.add_node("track_history", track_history_agent_node)
builder.add_node("track_history_tools", ToolNode(track_history_agent["tools"]))
builder.add_conditional_edges(
    'track_history',
    tools_condition,
    {"tools":"track_history_tools","__end__":"main" }
)
builder.add_edge("track_history_tools", "track_history")


# WHATSAPP
builder.add_node("whatsapp", whatsapp_agent_node)
builder.add_node("whatsapp_tools", ToolNode(whatsapp_agent["tools"]))
builder.add_conditional_edges(
    'whatsapp',
    tools_condition,
{"tools":"whatsapp_tools","__end__":"main" }
)
builder.add_edge("whatsapp_tools", "whatsapp")



#WHATSAPP_PRESENTATION_AGENT
builder.add_node("whatsapp_presentation_agent", whatsapp_presentation_agent_node)
builder.add_node("whatsapp_presentation_tools", ToolNode(whatsapp_presentation_agent["tools"]))
builder.add_conditional_edges(
    'whatsapp_presentation_agent',
    tools_condition,
{"tools":"whatsapp_presentation_tools","__end__":"main" }
)
builder.add_edge("whatsapp_presentation_tools", "whatsapp_presentation_agent")



builder.add_edge(START, "main")
builder.add_edge("main", "whatsapp")
builder.add_edge("main", "track_history")
builder.add_edge("main", "whatsapp_presentation_agent")


builder.add_edge("main",END  )

complex_graph = builder.compile()
