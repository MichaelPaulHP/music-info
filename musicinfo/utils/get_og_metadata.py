from bs4 import BeautifulSoup
import requests
from typing import Dict, Optional
from urllib.parse import urljoin



def get_og_metadata(url: str) -> Dict[str, str]:
    """
    Extrae los metadatos Open Graph de una URL, siguiendo redirecciones.

    Args:
        url (str): La URL inicial

    Returns:
        Tuple[Dict[str, str], str]: (metadatos OG encontrados, URL final)
    """
    try:
        # Configurar headers para simular un navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Realizar la petición HTTP permitiendo redirecciones
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            allow_redirects=True  # Importante: permite seguir redirecciones
        )
        response.raise_for_status()

        # Obtener la URL final después de redirecciones
        final_url = response.url

        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        og_data = {}

        # Buscar todas las etiquetas meta con propiedades OG
        meta_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))

        # Extraer los metadatos
        for tag in meta_tags:
            property_name = tag.get('property', '').replace('og:', '')
            content = tag.get('content')
            #print(f"Propiedad OG: {property_name} - Contenido: {content}")

            if property_name and content:
                # Si es una URL relativa, convertirla a absoluta usando la URL final
                if property_name in ['image', 'url'] and not content.startswith(('http://', 'https://')):
                    content = urljoin(final_url, content)

                og_data[property_name] = content

        # Si no hay título OG, intentar obtener el título normal
        if 'title' not in og_data:
            title_tag = soup.find('title')
            if title_tag:
                og_data['title'] = title_tag.string

        # Agregar la URL final a los metadatos
        og_data['final_url'] = final_url

        return og_data

    except requests.RequestException as e:
        raise Exception(f"Error al acceder a la URL: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al procesar los metadatos: {str(e)}")