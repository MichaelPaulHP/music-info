from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
import json
import re

def extraer_json(texto):
    # Buscar patrón de JSON en el texto
    patron_json = r'(\{.*\}|\[.*\])'
    coincidencia = re.search(patron_json, texto, re.DOTALL)

    if coincidencia:
        json_texto = coincidencia.group(0)
        try:
            return json.loads(json_texto)
        except json.JSONDecodeError:
            pass

    # Si llegamos aquí, no pudimos extraer un JSON válido
    raise ValueError("No se pudo extraer un JSON válido de la respuesta")

@tool
def format_json(json_input):
    """Format json to get a string friendly to read."""
    #llm = ChatOpenAI(model="gpt-4-turbo")
    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.6,

    )

    system_prompt = """
    Actúa como un Maestro del emoji y conversor de JSON.
    Tu tarea es convertir estructuras JSON en un texto plano bien formateado para ser enviado a WhatsApp.

    INSTRUCCIONES DE CONTENIDO:
    - Divide el contenido original en secciones lógicas  
    - Representa el contenido original sin alterarlo
    - Si un campo está vacío o es null, omítelo completamente
    - Asegúrate de que la división en strings mantenga la coherencia del contenido
    - Mantén un estilo consistente en todos los strings del array
    - Usar Emijos para representar los datos, emociones  y acciones.
    - El texto de ser amigable y agradable.
    - Responde solo que el texto que se requiere, SIN introducción,SIN explicación ,SIN texto adicional.
    
 
    """
    system_message = SystemMessage(content=system_prompt)
    user_message = HumanMessage(content=f'Formatear este JSON: {(json_input)}')
    response = llm.invoke([system_message, user_message])
    datos_raw = response.content
    return datos_raw
