from langchain_core.tools import tool

from musicinfo.models import SongInfo
from musicinfo.utils import song_info_to_arr


@tool
def build_song_history_whatsapp_template(song_json:SongInfo):
     """build whatsapp template message to send history song"""
     arr = song_info_to_arr(song_json)

     parameters = []


     for i, text in enumerate(arr):
         parameter = {
             "type": "text",
             "text": text,
             #"parameter_name": str(i + 1)  # Posición + 1 como string
         }
         parameters.append(parameter)
     #print(arr)
     print(f"build_history_template ")
     return {
        "template": "track_info",
        "components": [
            {
                "type": "body",
                "parameters": parameters
            }
        ]

     }
