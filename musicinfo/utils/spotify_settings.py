from functools import lru_cache

from .spotify_client import SpotifyConfig, SpotifyClient
import os


class SpotifySettings:
    """Configuración de la aplicación"""

    def __init__(self):

        self.spotify_config = SpotifyConfig(
            client_id=os.environ.get("SPOTIFY_CLIENT_ID", "TU_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET", "TU_CLIENT_SECRET")
        )
        print(self.spotify_config)


@lru_cache()
def get_settings():
    return SpotifySettings()

@lru_cache()
def get_spotify_client() -> SpotifyClient:
    settings = get_settings()
    return SpotifyClient(settings.spotify_config)

