from repositories.utils import extract_playlist_id, clear, cyan, bold
from repositories.sorter import reorder_playlist
from repositories.liker import like_tracks_from_playlist
from repositories.backup import create_backup, restore_backup
from repositories.doctor import doctor_playlist

import sys

def main_menu():
    clear()
    print(bold(cyan('\n🎧 --- MAIN MENU --- 🎧')))
    print('[1] Sort playlist')
    print('[2] Like all tracks in playlist')
    print('[3] Restore playlist from backup')
    print('[4] Create Playlist Backup')
    print('[5] Playlist doctor (find & fix duplicates/variants)')
    print('[0] Exit')
    print('-----------------')

    try:
        op = int(input('Pick an option: '))
    except Exception:
        print('Invalid option.')
        return

    match op:
        case 1:
            playlist_url = input('Playlist URL: ')
            playlist_id = extract_playlist_id(playlist_url)
            if playlist_id:
                try:
                    order_by = int(input('Sort by:\n[1] Alphabetical\n[2] Artist\n[3] Album\n[4] Artist-Albumn\nA: '))
                except Exception:
                    print('Invalid option.')
                    return
                reorder_playlist(playlist_id, order_by)
                input('🎉 Finished. Press Enter to continue...')
        case 2:
            playlist_url = input('Playlist URL: ')
            playlist_id = extract_playlist_id(playlist_url)
            if playlist_id:
                like_tracks_from_playlist(playlist_id)
                input('🎉 Finished. Press Enter to continue...')
        case 3:
            playlist_url = input('Playlist URL to restore: ')
            playlist_id = extract_playlist_id(playlist_url)
            if playlist_id:
                restore_backup(playlist_id)
                input('🎉 Finished. Press Enter to continue...')
        case 4:
            playlist_url = input('Playlist URL to backup: ')
            playlist_id = extract_playlist_id(playlist_url)
            if playlist_id:
                create_backup(playlist_id)
                input('🎉 Finished. Press Enter to continue...')
        case 5:
            playlist_url = input('Playlist URL: ')
            playlist_id = extract_playlist_id(playlist_url)
            if playlist_id:
                doctor_playlist(playlist_id)
                input('🎉 Finished. Press Enter to continue...')
        case 0:
            print('👋 Leaving...')
            sys.exit(0)
        case _:
            print('Invalid option')

if __name__ == '__main__':
    while True:
        main_menu()