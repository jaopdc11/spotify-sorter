import os
import csv
from .utils import sp, get_playlist_tracks, print_loading, green, yellow

BACKUP_DIR = 'backups'

def save_backup(playlist_id, tracks):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = f'{BACKUP_DIR}/{playlist_id}.csv'
    print_loading("Saving backup", "💾")
    with open(backup_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'artist', 'album'])
        writer.writeheader()
        for track in tracks:
            writer.writerow(track)
    print(green(f'✅ Backup saved at {backup_path}'))

def load_backup(playlist_id):
    backup_path = f'{BACKUP_DIR}/{playlist_id}.csv'
    print_loading("Loading backup", "📂")
    if not os.path.exists(backup_path):
        print(yellow('❌ Backup not found.'))
        return []
    tracks = []
    with open(backup_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tracks.append(row)
    print(green(f"✅ Loaded {len(tracks)} tracks from backup!"))
    return tracks

def create_backup(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    if not tracks:
        print(yellow('⚠️ Playlist is empty.'))
        return
    save_backup(playlist_id, tracks)
    print(green('🎉 Backup created!'))

def restore_backup(playlist_id):
    tracks = load_backup(playlist_id)
    if not tracks:
        print(yellow("⚠️ Nothing to restore."))
        return
    print_loading("Clearing playlist", "🧹")
    sp.playlist_replace_items(playlist_id, [])
    print_loading("Restoring backup", "♻️")
    uris = [f"spotify:track:{t['id']}" for t in tracks]
    chunk_size = 100
    for i in range(0, len(uris), chunk_size):
        print_loading(f"Restoring tracks {i+1} to {min(i+chunk_size, len(uris))}", "🔙", 0.7)
        sp.playlist_add_items(playlist_id, uris[i:i+chunk_size])
    print(green("✅ Backup restored!"))