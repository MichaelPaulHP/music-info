from typing import List, Callable

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from musicinfo.tools import (
    get_song_history,
    get_track_basic_info,
    get_track_info_from_url,
    build_whatsapp_error_template_message,
    build_song_history_whatsapp_template,
    send_simple_message,
    send_whatsapp_template
)

def format_langchain_tools(tools: List[Callable] ) -> str:
    formatted_text = ""

    for tool_func in tools:

        name = tool_func.name
        description = tool_func.description

        # Añadir punto final si no tiene
        if description and not description.endswith('.'):
            description += '.'

        formatted_text += f"{name}: {description}\n"

    return formatted_text.strip()


def get_full_tools_agent():
    """Create an agent."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    tools = [

        send_simple_message,
        send_whatsapp_template,

        get_track_info_from_url,
        get_track_basic_info,
        get_song_history,

        build_whatsapp_error_template_message,
        build_song_history_whatsapp_template,
    ]
    tool_names = format_langchain_tools(tools)
    system_message = f"""
    # ROL Y OBJETIVO
    Eres un asistente musical que conecta a usuarios con información sobre canciones vía WhatsApp.
    Tu misión es proporcionar datos históricos y contextuales sobre canciones, manteniendo al usuario informado de cada paso del proceso.

    # CANALES DE COMUNICACIÓN
    - Utilizas exclusivamente WhatsApp para todas las interacciones con el usuario

    # PROTOCOLO DE COMUNICACIÓN
    1. **ANTES DE ACTUAR**: Informa claramente "Voy a [acción específica]" antes de ejecutar cualquier herramienta.
    2. **DURANTE EL PROCESO**: Si una acción toma tiempo, envía "Estoy [descripción del proceso]..."
    3. **DESPUÉS DE ACTUAR**: Confirma "He completado [acción específica]" e inmediatamente comparte los resultados.
    4. **EN CASO DE ERROR**: Indica "No he podido [acción] porque [razón específica]" y ofrece alternativas.

    # TIPOS DE MENSAJES

    1. **Mensaje Simple**:
       - Propósito: Notificaciones sobre acciones o confirmaciones
       - Formato: Breve (máximo 2 líneas), tono conversacional y amigable
       - Ejemplo: "Voy a buscar información sobre 'Bohemian Rhapsody' de Queen."

    2. **Mensaje Template**:
       - Propósito: Enviar información completa sobre canciones o para errores
       - Formato: las herramienta hace el formato.
          

   
    # HERRAMIENTAS DISPONIBLES
    Puedes utilizar únicamente estas herramientas para obtener información:
    {tool_names}

  
    # RESTRICCIONES IMPORTANTES
    - NO busques información por tu cuenta bajo ninguna circunstancia
    - Utiliza ÚNICAMENTE las herramientas especificadas
    - Si faltan datos esenciales (artista, título), solicítalos amablemente al usuario
    - Nunca inventes información que no obtengas de las herramientas proporcionadas
    - Sé preciso en comunicar exactamente qué estás haciendo con cada herramienta
    - Ante falta de información, indica claramente qué datos no están disponibles

    # FLUJO DE CONVERSACIÓN TÍPICO
    1. Informas que vas a buscar datos básicos de la canción.      
    2. Informas que vas a buscar datos históricos
    3. Informas que estas preparando para que se vea bonito
    4. Informas que preparando el template.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "{system_message}"
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)

    return {"agent":(prompt | llm.bind_tools(tools)), "tools": tools }


#full_tools = create_agent()
# res = track_info_agent.invoke({"messages": [HumanMessage(content='dame la informacion basica de la cancion maría magdalena - Sandra ')]})
# print(res)
# print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
# res.pretty_print()
