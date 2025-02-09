import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv('config.env')

# Spotify API Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")

# Initialize Spotify client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE,
                                                open_browser=True))

def get_playlist_tracks(playlist_id):
    """Retrieve all tracks from the given playlist"""
    tracks = []
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results['items']:
            track = item.get('track')
            if track:
                tracks.append({
                    'name': track['name'],
                    'id': track['id'],
                    'artist': track['artists'][0]['name'],  # Get the artist's name
                    'album': track['album']['name'],  # Get the album name
                })
        results = sp.next(results)

    return tracks

def custom_sort_key(song_name):
    """Sort songs by numerical prefix first, then alphabetically"""
    match = re.match(r'^(\d+)', song_name) 
    if match:
        return (0, int(match.group()))  
    return (1, song_name.lower()) 

def reorder_playlist(playlist_id, order_by):
    tracks = get_playlist_tracks(playlist_id)

    if not tracks:
        print("No tracks to reorder in the playlist.")
        return

    # Use playlist_replace_items to clear the playlist by replacing all items with an empty list
    sp.playlist_replace_items(playlist_id, [])
    print("🎶 Playlist cleared...")

    match order_by:
        case 2:
            # Group by artist and sort each group by song name
            grouped_tracks = {}
            for track in tracks:
                artist = track['artist']
                if artist not in grouped_tracks:
                    grouped_tracks[artist] = []
                grouped_tracks[artist].append(track)

            # Sort each group alphabetically by song name
            for artist in grouped_tracks:
                grouped_tracks[artist].sort(key=lambda x: custom_sort_key(x['name']))

            # Flatten the list back together
            sorted_tracks = [track for artist in sorted(grouped_tracks) for track in grouped_tracks[artist]]

        case 3:
            # Group by album and sort each group by song name
            grouped_tracks = {}
            for track in tracks:
                album = track['album']
                if album not in grouped_tracks:
                    grouped_tracks[album] = []
                grouped_tracks[album].append(track)

            # Sort each group alphabetically by song name
            for album in grouped_tracks:
                grouped_tracks[album].sort(key=lambda x: custom_sort_key(x['name']))

            # Flatten the list back together
            sorted_tracks = [track for album in sorted(grouped_tracks) for track in grouped_tracks[album]]

        case _:
            # Default: alphabetical sorting by song name
            sorted_tracks = sorted(tracks, key=lambda x: custom_sort_key(x['name']))

    track_uris = [f"spotify:track:{track['id']}" for track in sorted_tracks]

    # Split the track URIs into chunks of 100
    chunk_size = 100
    for i in range(0, len(track_uris), chunk_size):
        track_uris_chunk = track_uris[i:i + chunk_size]
        sp.playlist_add_items(playlist_id, track_uris_chunk)
        print(f"Added tracks {i+1} to {min(i+chunk_size, len(track_uris))}...")

    print("✅ Playlist reordered successfully!")

def extract_playlist_id(playlist_url):
    """Extract the playlist ID from the Spotify URL"""
    match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
    if match:
        return match.group(1)
    else:
        print("Invalid Spotify playlist URL.")
        return None

# Get the playlist link and the order criteria from the user
playlist_url = input("Enter the playlist URL: ")
order_by = int(input("How would you like to organize the playlist?\n[1] Alphabetical\n[2] Artist\n[3] Album\nR:     "))
playlist_id = extract_playlist_id(playlist_url)

if playlist_id:
    reorder_playlist(playlist_id, order_by)
