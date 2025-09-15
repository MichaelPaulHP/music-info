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
    Tu tarea es convertir estructuras JSON en un NUEVO OBJETO JSON que tenga la siguiente estructura específica:
    {
      "WhatsApp": [
        "mensaje formateado 1",
        "mensaje formateado 2",
        "mensaje formateado 3"
      ]
    }

    INSTRUCCIONES DE FORMATO JSON:
    - El objeto JSON de salida DEBE contener exactamente un atributo llamado "WhatsApp"
    - El valor de "WhatsApp" DEBE ser un array de strings
    - Cada string en el array debe ser un fragmento bien formateado del contenido JSON original
    - Debes devolver un objeto JSON válido y parseable

    INSTRUCCIONES PARA CADA STRING DEL ARRAY:
    - Cada string debe representar una sección lógica del JSON original
    - Añade emojis relevantes junto a cada categoría
    - Convierte las claves JSON originales en títulos amigables
    - Ningún string debe contener caracteres de nueva línea (\\n) ni tabulaciones (\\t)
    - Evita más de 4 espacios consecutivos en cualquier string
    - Ningún string individual debe exceder los 4000 caracteres

    INSTRUCCIONES DE CONTENIDO:
    - Divide el contenido original en secciones lógicas para crear el array
    - Mantén el contenido original sin alterarlo
    - Si un campo está vacío o es null, omítelo completamente
    - Asegúrate de que la división en strings mantenga la coherencia del contenido
    - Mantén un estilo consistente en todos los strings del array

    VERIFICACIÓN FINAL OBLIGATORIA:
    - Asegúrate de que el resultado sea un objeto JSON válido con la estructura especificada
    - Verifica que cada string en el array "WhatsApp" no contenga caracteres de nueva línea o tabulación
    - Confirma que no haya secuencias de más de 4 espacios en ningún string del array
    """
    system_message = SystemMessage(content=system_prompt)
    user_message = HumanMessage(content=f'formatear JSON: {(json_input)}')
    response = llm.invoke([system_message, user_message])
    datos_raw = response.content

    # Eliminar la primera línea que contiene '''json
    lineas = datos_raw.split('\n')
    json_contenido = '\n'.join(lineas[1:])  # Elimina la primera línea

    # Ahora parseamos el JSON
    try:
        datos = extraer_json(json_contenido)

        # Acceder a los valores
        whatsapp_data = datos["WhatsApp"]

        return whatsapp_data

    except json.JSONDecodeError as e:
        print(f"Error al parsear el JSON: {e}")
        return []
