from typing import List, TypedDict, Literal, Callable, NotRequired, Annotated

from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, create_react_agent
from langgraph.prebuilt import ToolNode

class Metadata(TypedDict):
    artist: NotRequired[str]
    song: NotRequired[str]

class SongInfo(TypedDict):
    metadata: NotRequired[Metadata]
    general_description: NotRequired[str]
    history: NotRequired[str]
    lyrics_analysis: NotRequired[str]
    highlighted_phrases: NotRequired[List[str]]
    fun_facts: NotRequired[List[str]]
    similar_songs: NotRequired[List[str]]
    genres: NotRequired[List[str]]
    related_genres: NotRequired[List[str]]
    other: NotRequired[str]


def format_song_info_with_emojis(song_info: SongInfo) -> list[str]:
    """
    Convierte un objeto SongInfo en un arreglo de strings con emojis.
    Cada string representa un atributo y los elementos de las listas se separan con emojis.

    Args:
        song_info: El objeto SongInfo a formatear

    Returns:
        Una lista de strings formateados con emojis
    """
    result = []

    # Procesar metadata si existe
    if "metadata" in song_info and song_info["metadata"]:
        metadata = song_info["metadata"]
        if "artist" in metadata:
            result.append(f"🎤 Artist: {metadata['artist']}")
        if "song" in metadata:
            result.append(f"🎵 Song: {metadata['song']}")

    # Procesar campos de texto simple
    if "general_description" in song_info:
        result.append(f"📝 General Description: {song_info['general_description']}")

    if "history" in song_info:
        result.append(f"🕰️ History: {song_info['history']}")

    if "lyrics_analysis" in song_info:
        result.append(f"📚 Lyrics Analysis: {song_info['lyrics_analysis']}")

    # Procesar listas
    if "highlighted_phrases" in song_info and song_info["highlighted_phrases"]:
        phrases = " ✨ ".join(song_info["highlighted_phrases"])
        result.append(f"💫 Highlighted Phrases: {phrases}")

    if "fun_facts" in song_info and song_info["fun_facts"]:
        facts = " ✨ ".join(song_info["fun_facts"])
        result.append(f"🎯 Fun Facts: {facts}")

    if "similar_songs" in song_info and song_info["similar_songs"]:
        similar = " ✨ ".join(song_info["similar_songs"])
        result.append(f"👯 Similar Songs: {similar}")

    if "genres" in song_info and song_info["genres"]:
        genres = " ✨ ".join(song_info["genres"])
        result.append(f"🎧 Genres: {genres}")

    if "related_genres" in song_info and song_info["related_genres"]:
        related = " ✨ ".join(song_info["related_genres"])
        result.append(f"🔄 Related Genres: {related}")

    if "other" in song_info:
        result.append(f"ℹ️ Other: {song_info['other']}")

    return result

@tool
def send_simple_message(message, phone_number):
    """ Envia un mensaje simple a un phone number de whatsapp
    """
    print(f"WHATSAPP: ${message} ")
    return "Success"

@tool
def send_template(template_name, template_components):
    """ Envia un template message to whatsapp
    """
    print(f"WHATSAPP: ${template_name}  ${template_components}")
    return "Success"
@tool
def get_track_basic_info(song_raw):
    """Extract basic song info (name and artist) from text."""
    print(f"Getting basic info ${song_raw} ....")
    return """json
    {
        "artist": "The Monkees",
        "song":"I'm a Believer"
    }"""

@tool
def get_song_story_with_emojis(artists: str, song: str):
    """Retrieves song history and returns emoji-enhanced JSON."""
    print(f"Getting song history ${artists} ${song} ")
    return {
        "metadata": {
            "artist": "The Monkees",
            "song": "I'm a Believer"
        },
        "general_description": "La canción 'I'm a Believer', interpretada por The Monkees, es un himno pop sobre el amor y los giros inesperados que nos hacen pasar del escepticismo al fervor apasionado.",
        "history": "Lanzada en 1966, 'I'm a Believer' fue escrita por Neil Diamond. En medio de la explosión del rock de los años 60, The Monkees, una banda creada para un programa de televisión, capturó la atención del público con su carismático sonido pop. La canción rápidamente alcanzó el número uno en las listas de Billboard, y más tarde tuvo una resurgencia en popularidad cuando Smash Mouth la versionó para la película 'Shrek' en el 2000.",
        "lyrics_analysis": "La letra cuenta la historia de alguien que inicia escéptico sobre el amor, descartándolo como algo real, hasta que una experiencia personal le cambia la perspectiva. El tema principal gira en torno al poder transformador del amor y la capacidad de hacer que incluso los escépticos más duros se conviertan en 'creyentes'.",
        "highlighted_phrases": [
            "Then I saw her face, now I'm a believer (Entonces vi su rostro, y ahora soy un creyente)",
            "Not a trace of doubt in my mind (Ni un rastro de duda en mi mente)"
        ],
        "fun_facts": [
            "Fue la canción más vendida de 1967 en EE.UU.",
            "Neil Diamond grabó su propia versión antes del lanzamiento de The Monkees.",
            "El grupo The Monkees fue creado inicialmente para una serie de televisión del mismo nombre."
        ],
        "similar_songs": [
            "The Beatles - She Loves You",
            "The Turtles - Happy Together",
            "Herman's Hermits - I'm into Something Good",
            "The Beach Boys - Wouldn't It Be Nice",
            "Gerry and the Pacemakers - How Do You Do It?"
        ],
        "genres": [
            "Pop rock"
        ],
        "related_genres": [
            "Rock and roll",
            "Bubblegum pop"
        ],
        "other": "La canción, con su pegajosa melodía y tema optimista, ayudó a cimentar la reputación de The Monkees como una de las bandas más queridas de los años 60, dejando una marca indeleble en la cultura pop estadounidense."
    }

@tool
def build_whatsapp_error_template_message(message: str):
    """build a whatsapp template message to send an error """
    print(f"build_error_template ")
    return {
    "template": "error_template",
    "components":[message]
    }


@tool
def build_song_history_whatsapp_template(song_json:SongInfo):
     """build whatsapp template message to send history song"""
     arr = format_song_info_with_emojis(song_json)

     print(arr)
     print(f"build_history_template ")
     return {
        "template": "song_history",
        "components": arr
     }

tools = [

    send_simple_message,
    send_template,

    get_track_basic_info,
    get_song_story_with_emojis,

    build_whatsapp_error_template_message,
    build_song_history_whatsapp_template,
]


def format_langchain_tools(tools: List[Callable]) -> str:
    formatted_text = ""

    for tool_func in tools:

        name = tool_func.name
        description = tool_func.description

        # Añadir punto final si no tiene
        if description and not description.endswith('.'):
            description += '.'

        formatted_text += f"{name}: {description}\n"

    return formatted_text.strip()


tool_names = format_langchain_tools(tools)

#TODO: phone nummber set as state => add un first human message.
#TODO:: pasar el jhson a array
system_message = f"""
    # ROL Y OBJETIVO
    Eres un asistente intermediario amigable que conecta usuarios con información musical a través de WhatsApp.
    Tu misión es informar al usuario de tus tareas que haces  y enviar información historica de la canción.

    # FUNCIONES PRINCIPALES
    1. SIEMPRE notificar al usuario de lo que vas a hacer
    2. SIEMPRE notificar al usuario de lo que hiciste
    3. Enviar información histórica detallada de canciones solicitadas
    4. Manejar errores o falta de información de forma amable y constructiva
    
    

    # CANALES DE COMUNICACIÓN
    - Utiliza exclusivamente WhatsApp para todas las interacciones con el usuario

    # TIPOS DE MENSAJES
    1. **Mensaje Simple**: 
       - Propósito: Notificaciones sobre acciones a hacer o acciones completadas
       - Formato: Breve, informal y amigable
   
    2. **Mensaje Template**:
       - Propósito: Enviar información completa sobre canciones o reportar errores
       - Formato: formato ya definido en WhatsApp, solo construir el template

    # RESTRICCIONES IMPORTANTES
    - NO busques información por tu cuenta bajo ninguna circunstancia
    - Utiliza ÚNICAMENTE las herramientas especificadas: 
        {tool_names}
    - Si faltan datos esenciales (artista, título), solicítalos amablemente al usuario
    - Nunca inventes información que no obtengas de las herramientas proporcionadas.
 
    """


sys_msg = SystemMessage(content=system_message)

llm = ChatOpenAI(model="gpt-4o")
# llm = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature=0.1,
# )
#
llm_with_tools = llm.bind_tools(tools)

class MyState(MessagesState):
     song_json: NotRequired[dict[str, list | str]]


def whatsapp_agent_node(state: MyState):
    last_message = state['messages'][-1]
    song_json = None
    # if last_message and isinstance(last_message, ToolMessage):
    #     song_json = last_message.content
    message = llm_with_tools.invoke([sys_msg] + state["messages"]);
    if isinstance(message, ToolMessage):
        print(message.id)
    return {"messages": [message],"song_json":song_json}


builder = StateGraph(MessagesState)
builder.add_node("main", whatsapp_agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "main")
builder.add_conditional_edges(
    'main',
    tools_condition
)
builder.add_edge("tools", "main")
builder.add_edge("main",END  )

tools_graph = builder.compile()