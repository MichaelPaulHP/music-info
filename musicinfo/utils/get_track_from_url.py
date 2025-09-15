from .get_og_metadata import get_og_metadata
from .is_spotify_url import is_spotify_url
from .spotify_settings import get_spotify_client




def get_track_from_url(url):
    is_spotify,_ = is_spotify_url(url)
    if is_spotify:
        spotify_client = get_spotify_client()
        return  spotify_client.get_track_info(str(url))
    else:
        return get_og_metadata(url)

