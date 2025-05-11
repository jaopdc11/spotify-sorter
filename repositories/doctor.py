from .utils import sp, get_playlist_tracks, green, yellow, red, cyan, bold, print_loading
from .backup import save_backup

def find_duplicates(tracks):
    # Group all tracks with same name+artist
    groups = {}
    for idx, track in enumerate(tracks):
        key = (track['name'].strip().lower(), track['artist'].strip().lower())
        groups.setdefault(key, []).append(idx)
    # Only keep groups with more than one occurrence
    return [indices for indices in groups.values() if len(indices) > 1]

def find_album_variants(tracks):
    # Same name + artist, but different album
    variants = {}
    for idx, track in enumerate(tracks):
        key = (track['name'].strip().lower(), track['artist'].strip().lower())
        variants.setdefault(key, []).append((idx, track['album'].strip().lower()))
    result = []
    for key, lst in variants.items():
        albums = set(album for _, album in lst)
        if len(albums) > 1:
            result.append([i for i, _ in lst])
    return result

def show_track(track, idx):
    print(f"{cyan(f'[{idx}]')} {bold(track['name'])} - {green(track['artist'])} {yellow('('+track['album']+')')}")

def remove_tracks_from_playlist(playlist_id, tracks, indices):
    uris = [{"uri": f"spotify:track:{tracks[i]['id']}", "positions": [i]} for i in indices]
    print_loading("Removing selected tracks", "🗑️")
    sp.playlist_remove_specific_occurrences_of_items(playlist_id, uris)
    print(green("✅ Tracks removed!"))

def doctor_playlist(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    if not tracks:
        print(yellow("⚠️ Playlist is empty."))
        return

    print_loading("Saving backup before making changes", "💾")
    save_backup(playlist_id, tracks)

    to_remove_indices = set()

    print(bold(cyan("\n🔎 Checking for exact duplicates...")))
    duplicate_groups = find_duplicates(tracks)
    if not duplicate_groups:
        print(green("✅ No exact duplicates found!"))
    else:
        for group in duplicate_groups:
            group = [idx for idx in group if idx not in to_remove_indices]
            if len(group) <= 1:
                continue
            print("\nFound duplicates:")
            for idx in group:
                show_track(tracks[idx], idx)
            ans = input(red("Do you want to remove one or more? (y/n): ")).strip().lower()
            if ans == 'y':
                print("Type the indices to remove, separated by space (leave at least one):")
                to_remove = input("Indices to remove: ").strip().split()
                indices = [int(i) for i in to_remove if i.isdigit() and int(i) in group]
                if indices and len(indices) < len(group):
                    to_remove_indices.update(indices)
                else:
                    print(yellow("Skipped or tried to remove all duplicates (not allowed)."))

    print(bold(cyan("\n🔎 Checking for album variants (same song, different album)...")))
    variants = find_album_variants(tracks)
    if not variants:
        print(green("✅ No album variants found!"))
    else:
        for group in variants:
            group = [idx for idx in group if idx not in to_remove_indices]
            if len(group) <= 1:
                continue
            print("\nFound album variants:")
            for idx in group:
                show_track(tracks[idx], idx)
            ans = input(red("Do you want to remove one or more? (y/n): ")).strip().lower()
            if ans == 'y':
                print("Type the indices to remove, separated by space (leave at least one):")
                for idx in group:
                    show_track(tracks[idx], idx)
                to_remove = input("Indices to remove: ").strip().split()
                indices = [int(i) for i in to_remove if i.isdigit() and int(i) in group]
                if indices and len(indices) < len(group):
                    to_remove_indices.update(indices)
                else:
                    print(yellow("Skipped or tried to remove all variants (not allowed)."))

    if to_remove_indices:
        indices_sorted = sorted(to_remove_indices, reverse=True)
        remove_tracks_from_playlist(playlist_id, tracks, indices_sorted)
    else:
        print(yellow("No tracks selected for removal."))

    print(green("\n🎉 Playlist checkup complete!"))

if __name__ == "__main__":
    playlist_url = input("Playlist URL: ")
    from .utils import extract_playlist_id
    playlist_id = extract_playlist_id(playlist_url)
    if playlist_id:
        doctor_playlist(playlist_id)