from musicinfo.models import SongInfo


def  song_info_to_arr(song_info: SongInfo) -> list[str]:
    result = []

    # Procesar metadata si existe
    if hasattr(song_info, "metadata") and song_info.metadata:
        metadata = song_info.metadata
        if hasattr(metadata, "artist") and metadata.artist:
            result.append(f"🎤 Artist: {metadata.artist}")
        if hasattr(metadata, "song") and metadata.song:
            result.append(f"🎵 Song: {metadata.song}")

    # Procesar campos de texto simple
    if hasattr(song_info, "general_description") and song_info.general_description:
        result.append(f"📝 General Description: {song_info.general_description}")

    if hasattr(song_info, "history") and song_info.history:
        result.append(f"🕰️ History: {song_info.history}")

    if hasattr(song_info, "lyrics_analysis") and song_info.lyrics_analysis:
        result.append(f"📚 Lyrics Analysis: {song_info.lyrics_analysis}")

    # Procesar listas
    if hasattr(song_info, "highlighted_phrases") and song_info.highlighted_phrases:
        phrases = " ✨ ".join(song_info.highlighted_phrases)
        result.append(f"💫 Highlighted Phrases: {phrases}")

    if hasattr(song_info, "fun_facts") and song_info.fun_facts:
        facts = " ✨ ".join(song_info.fun_facts)
        result.append(f"🎯 Fun Facts: {facts}")

    if hasattr(song_info, "similar_songs") and song_info.similar_songs:
        similar = " ✨ ".join(song_info.similar_songs)
        result.append(f"👯 Similar Songs: {similar}")

    if hasattr(song_info, "genres") and song_info.genres:
        genres = " ✨ ".join(song_info.genres)
        result.append(f"🎧 Genres: {genres}")

    if hasattr(song_info, "related_genres") and song_info.related_genres:
        related = " ✨ ".join(song_info.related_genres)
        result.append(f"🔄 Related Genres: {related}")

    if hasattr(song_info, "other") and song_info.other:
        result.append(f"ℹ️ Other: {song_info.other}")

    field_required_count = 11
    while len(result) < field_required_count:
        result.append('📝')

    return result
