from typing import Dict, Optional
import requests
from datetime import datetime, timedelta
import base64
from urllib.parse import urlparse
from pydantic import BaseModel

class SpotifyConfig(BaseModel):
    """Configuración para la API de Spotify"""
    client_id: str
    client_secret: str
    token_url: str = "https://accounts.spotify.com/api/token"
    api_base_url: str = "https://api.spotify.com/v1"


class SpotifyClient:
    def __init__(self, config: SpotifyConfig):
        self.config = config
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

    def _get_authorization_header(self) -> str:
        """Genera el header de autorización para obtener el token"""
        auth_string = f"{self.config.client_id}:{self.config.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        return f"Basic {auth_base64}"

    def _refresh_token_if_needed(self) -> None:
        """Actualiza el token si ha expirado o no existe"""
        now = datetime.now()

        if (not self._access_token or
                not self._token_expires_at or
                now >= self._token_expires_at):
            headers = {
                "Authorization": self._get_authorization_header(),
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {"grant_type": "client_credentials"}

            response = requests.post(
                self.config.token_url,
                headers=headers,
                data=data
            )
            response.raise_for_status()

            token_data = response.json()
            self._access_token = token_data["access_token"]
            # Restamos 60 segundos para renovar antes de que expire
            self._token_expires_at = now + timedelta(seconds=token_data["expires_in"] - 60)

    def _extract_track_id(self, spotify_url: str) -> str:
        """Extrae el ID de la canción de una URL de Spotify"""
        path = urlparse(spotify_url).path
        return path.split('/')[-1].split('?')[0]

    def get_track_info(self, track_url: str) -> Dict:
        """
        Obtiene la información detallada de una canción

        Args:
            track_url: URL de Spotify de la canción

        Returns:
            Dict con la información de la canción
        """
        self._refresh_token_if_needed()

        track_id = self._extract_track_id(track_url)

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json"
        }

        response = requests.get(
            f"{self.config.api_base_url}/tracks/{track_id}",
            headers=headers
        )
        response.raise_for_status()

        track_data = response.json()

        # Formatear la respuesta
        return {
            "id": track_data["id"],
            "name": track_data["name"],
            "artists": [
                {
                    "name": artist["name"],
                    "id": artist["id"]
                } for artist in track_data["artists"]
            ],
            #"album": {
            #     "name": track_data["album"]["name"],
            #     "id": track_data["album"]["id"],
            #     "release_date": track_data["album"]["release_date"],
            #     "total_tracks": track_data["album"]["total_tracks"],
            #     "images": track_data["album"]["images"]
            # },
            #"duration_ms": track_data["duration_ms"],
            #"explicit": track_data["explicit"],
            #"popularity": track_data["popularity"],
            #"preview_url": track_data["preview_url"],
            #"external_urls": track_data["external_urls"],
            #"available_markets": track_data["available_markets"]
        }



