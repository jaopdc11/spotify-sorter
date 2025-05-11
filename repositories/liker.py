from .utils import sp, get_playlist_tracks, green, yellow, print_loading

def like_tracks_from_playlist(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    if not tracks:
        print(yellow("⚠️ Playlist is empty, nothing to like."))
        return
    ids = [t['id'] for t in tracks]
    chunk_size = 50
    for i in range(0, len(ids), chunk_size):
        print_loading(f"Liking tracks {i+1} to {min(i+chunk_size, len(ids))}", "❤️", 0.7)
        sp.current_user_saved_tracks_add(ids[i:i+chunk_size])
    print(green("👍 All tracks liked!"))