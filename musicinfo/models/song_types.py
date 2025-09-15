from typing import List, Optional
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    artist: Optional[str] = Field(
        default=None,
        description="Nombre del artista o banda que interpreta la canción"
    )
    song: Optional[str] = Field(
        default=None,
        description="Nombre oficial de la canción"
    )


class SongInfo(BaseModel):
    metadata: Optional[Metadata] = Field(
        default=None,
        description="Información básica sobre el artista y la canción"
    )

    general_description: Optional[str] = Field(
        default=None,
        description="Explicación concisa sobre el tema central y significado de la canción"
    )

    history: Optional[str] = Field(
        default=None,
        description="Contexto histórico y origen de la canción, incluyendo fecha de lanzamiento y eventos relevantes"
    )

    lyrics_analysis: Optional[str] = Field(
        default=None,
        description="Interpretación detallada del significado de la letra, sus temas principales"
    )

    highlighted_phrases: Optional[List[str]] = Field(
        default=None,
        description="Lista de las frases más significativas o populares de la canción"
    )

    fun_facts: Optional[List[str]] = Field(
        default=None,
        description="Lista de datos interesantes y poco conocidos sobre la canción"
    )

    similar_songs: Optional[List[str]] = Field(
        default=None,
        description="Lista de 3-5 canciones similares con formato 'artista - canción'"
    )

    genres: Optional[List[str]] = Field(
        default=None,
        description="Géneros musicales principales de la canción"
    )

    related_genres: Optional[List[str]] = Field(
        default=None,
        description="Géneros musicales similares o influenciados"
    )

    other: Optional[str] = Field(
        default=None,
        description="Información adicional que un experto musicólogo consideraría relevante incluir"
    )