import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv('config.env')  # Make sure your .env file is in the same directory as your script

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
            track = item.get('track')  # Use .get() to avoid NoneType errors
            if track:  # Skip if 'track' is None
                tracks.append({
                    'name': track['name'],
                    'id': track['id']
                })
        results = sp.next(results)  # Fetch next page (if available)

    return tracks

def custom_sort_key(song_name):
    match = re.match(r'^(\d+)', song_name)  # Match numbers at the beginning of the title
    if match:
        return (0, int(match.group()))  # Sort numbers first in ascending order
    return (1, song_name.lower())  # Sort alphabetically if it's only text

def reorder_playlist(playlist_id):
    tracks = get_playlist_tracks(playlist_id)

    if not tracks:
        print("No tracks to reorder in the playlist.")
        return

    sorted_tracks = sorted(tracks, key=lambda x: custom_sort_key(x['name']))

    track_uris = [f"spotify:track:{track['id']}" for track in sorted_tracks]
    sp.playlist_replace_items(playlist_id, track_uris)

    print("✅ Playlist reordered successfully!")

playlist_id = input("Enter the playlist ID:     ")  # Prompt the user for the playlist ID
reorder_playlist(playlist_id)
