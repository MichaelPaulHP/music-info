from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_track_basic_info(song_raw):
    """Extract basic song info (name and artist) from text."""
    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
    system_prompt = """
    Actúa como un experto musical. Tu tarea es extraer únicamente el nombre del artista y el título de la canción de cualquier texto proporcionado, ignorando toda información adicional.
    Devuelve la información en el siguiente formato JSON:
    {
        "artist": "nombre del artista",
        "song": "título de la canción"
    }

    Reglas:
    - Si el texto contiene múltiples artistas o canciones, extrae solo los principales
    - Mantén los nombres exactamente como aparecen en el texto
    - Si no puedes identificar algún dato con certeza, usa null como valor
    """
    system_message = SystemMessage(content=system_prompt )
    user_message = HumanMessage(content=song_raw)
    response = llm.invoke([system_message, user_message])

    return response.content