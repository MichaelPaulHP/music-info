from typing import Tuple
from urllib.parse import urlparse
import re


def is_spotify_url(url: str) -> Tuple[bool, str]:
    """
    Valida si una URL es una URL válida de Spotify.

    Args:
        url (str): URL a validar

    Returns:
        Tuple[bool, str]: (es_valida, tipo_o_error)
            es_valida: True si es una URL válida de Spotify
            tipo_o_error: Si es válida, retorna el tipo ('track', 'album', 'playlist', etc.)
                         Si no es válida, retorna el mensaje de error
    """
    try:
        # Validar que la URL no está vacía
        if not url or not isinstance(url, str):
            return False, "URL debe ser un string no vacío"

        # Asegurarse que la URL empiece con http:// o https://
        if not url.startswith(('http://', 'https://')):
            return False, "URL debe empezar con http:// o https://"

        # Parsear la URL
        parsed = urlparse(url)

        # Validar dominio de Spotify - TIENE que ser exactamente estos dominios
        if parsed.netloc not in ['open.spotify.com']:
            return False, "Dominio inválido. Solo se acepta: open.spotify.com"

        # Patrones específicos de Spotify con límites exactos
        spotify_patterns = {
            'track': r'^/track/[A-Za-z0-9]{22}(?:\?|$)',
            'album': r'^/album/[A-Za-z0-9]{22}(?:\?|$)',
            'playlist': r'^/playlist/[A-Za-z0-9]{22}(?:\?|$)',
            'artist': r'^/artist/[A-Za-z0-9]{22}(?:\?|$)',
            'episode': r'^/episode/[A-Za-z0-9]{22}(?:\?|$)',
            'show': r'^/show/[A-Za-z0-9]{22}(?:\?|$)'
        }

        # Verificar el path contra los patrones
        for content_type, pattern in spotify_patterns.items():
            if re.match(pattern, parsed.path):
                return True, content_type

        return False, "URL no corresponde a un recurso válido de Spotify"

    except Exception as e:
        return False, f"Error de validación: {str(e)}"

