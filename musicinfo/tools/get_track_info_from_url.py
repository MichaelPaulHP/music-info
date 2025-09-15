from langchain_core.tools import tool

from musicinfo.utils import get_track_from_url


@tool
def get_track_info_from_url(url):
    """get song name and artist from an url."""
    return  get_track_from_url(url)