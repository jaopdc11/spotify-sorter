import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import re
import sys
import time

# Load environment variables
load_dotenv('config/.env')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = os.getenv('SCOPE')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=True
))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Color helpers
def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def green(text): return color(text, '92')
def yellow(text): return color(text, '93')
def red(text): return color(text, '91')
def blue(text): return color(text, '94')
def cyan(text): return color(text, '96')
def bold(text): return color(text, '1')

def print_loading(msg, emoji="⏳", duration=1.5):
    print(f"{emoji} {cyan(msg)}", end='', flush=True)
    for _ in range(3):
        time.sleep(duration/3)
        print('.', end='', flush=True)
    print()

def extract_playlist_id(playlist_url):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", playlist_url)
    if match:
        return match.group(1)
    else:
        print(red('❌ Invalid playlist URL.'))
        return None

def get_playlist_tracks(playlist_id):
    playlist = sp.playlist(playlist_id, fields="name")
    playlist_name = playlist.get("name", "Unknown Playlist")
    print_loading(f"Fetching tracks from '{playlist_name}'...", "🎵")
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results['items']:
            track = item.get('track')
            if track:
                tracks.append({
                    'name': track['name'],
                    'id': track['id'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                })
        results = sp.next(results)
    print(green(f"✅ Found {len(tracks)} tracks!"))
    return tracks

def custom_sort_key(song_name):
    match = re.match(r'^(\d+)', song_name)
    if match:
        return (0, int(match.group()))
    return (1, song_name.lower())