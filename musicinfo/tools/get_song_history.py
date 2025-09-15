from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from musicinfo.models import SongInfo


@tool
def get_song_history(artists: str, song: str)->SongInfo:
    """get song history from song name and artist name."""
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    # llm = ChatDeepSeek(
    #     model="deepseek-chat",
    #     temperature=0.6,
    # )
    structured_llm = llm.with_structured_output(SongInfo)
    system_prompt = """
    Actúa como un experto musicólogo con profundo conocimiento en historia musical y 
    como un Maestro del emoji 
    Tu tarea es proporcionar información de manera apasionado de la cancion "artista - canción".
     
    Reglas importantes:
    - La información debe sentirse como una conversación con un amigo apasionado por la música que comparte su conocimiento de manera natural y entretenida.
    - Hacer una descripción emotiva.
    - trata de usar emojis para expresar tu emoción  
    - Siempre usa emojis en tus respuestas. 
    - Mantén las respuestas objetivas y basadas en hechos verificables. 
    - Incluye solo curiosidades relevantes y verificables.
    - Las recomendaciones deben basarse en similitud musical o temática.
    - Agregar la traducción al español entre paréntesis de las frases que no estan en español.
    - Si no hay información verificable para algún campo, usa null como valor.
    """


    system_message = SystemMessage(content=system_prompt)
    user_message = HumanMessage(content=f'{artists} - {song}')
    response = structured_llm.invoke([system_message, user_message])

    return response
