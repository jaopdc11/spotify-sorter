from .utils import sp, get_playlist_tracks, custom_sort_key, green, yellow, print_loading
from .backup import save_backup

def reorder_playlist(playlist_id, order_by):
    tracks = get_playlist_tracks(playlist_id)
    if not tracks:
        print(yellow('⚠️ Playlist is empty.'))
        return

    save_backup(playlist_id, tracks)

    print_loading("Clearing playlist", "🧹")
    sp.playlist_replace_items(playlist_id, [])
    print(green('✅ Playlist cleared.'))

    print_loading("Sorting tracks", "🔀")
    if order_by == 2:
        grouped = {}
        for t in tracks:
            grouped.setdefault(t['artist'], []).append(t)
        for artist in grouped:
            grouped[artist].sort(key=lambda x: custom_sort_key(x['name']))
        sorted_tracks = [t for artist in sorted(grouped, key=custom_sort_key) for t in grouped[artist]]
    elif order_by == 3:
        grouped = {}
        for t in tracks:
            grouped.setdefault(t['album'], []).append(t)
        for album in grouped:
            grouped[album].sort(key=lambda x: custom_sort_key(x['name']))
        sorted_tracks = [t for album in sorted(grouped, key=custom_sort_key) for t in grouped[album]]
    elif order_by == 4:
        artist_grouped = {}
        for t in tracks:
            artist_grouped.setdefault(t['artist'], []).append(t)
        sorted_tracks = []
        for artist in sorted(artist_grouped, key=custom_sort_key):
            album_grouped = {}
            for t in artist_grouped[artist]:
                album_grouped.setdefault(t['album'], []).append(t)
            for album in sorted(album_grouped, key=custom_sort_key):
                album_tracks = sorted(album_grouped[album], key=lambda x: custom_sort_key(x['name']))
                sorted_tracks.extend(album_tracks)
    else:
        sorted_tracks = sorted(tracks, key=lambda x: custom_sort_key(x['name']))

    uris = [f"spotify:track:{t['id']}" for t in sorted_tracks]
    chunk_size = 100
    for i in range(0, len(uris), chunk_size):
        print_loading(f"Adding tracks {i+1} to {min(i+chunk_size, len(uris))}", "➕", 0.7)
        sp.playlist_add_items(playlist_id, uris[i:i+chunk_size])

    print(green('🎉 Playlist reordered!'))