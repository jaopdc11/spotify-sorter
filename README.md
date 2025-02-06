
# Spotify Playlist Organizer

This Python script allows you to reorder tracks in a Spotify playlist based on a custom sorting logic. It uses the Spotify API to fetch the tracks and reorder them. The script sorts the playlist such that numbers come first in ascending order, followed by alphabetical sorting for the rest of the track names.

## Features

- Reorders tracks in a Spotify playlist.
- Sorts tracks by numbers first (ascending order) and then alphabetically.
- Uses the Spotify API for authentication and playlist management.
- Configuration settings are loaded from a `.env` file for security.

## Prerequisites

Before using the script, make sure you have:

- A Spotify developer account and created an app to get your `CLIENT_ID` and `CLIENT_SECRET`.
- Python 3.x installed on your machine.
- The following Python libraries installed:
  - `spotipy` for interacting with the Spotify API.
  - `python-dotenv` for loading environment variables from a `.env` file.

## Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/jaopdc11/spotify-playlist-organizer.git
    cd spotify-playlist-organizer
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root of the project and add your Spotify credentials:
    ```
    CLIENT_ID=your_spotify_client_id
    CLIENT_SECRET=your_spotify_client_secret
    REDIRECT_URI=http://localhost:8888/callback
    SCOPE=playlist-modify-public playlist-modify-private
    ```

4. Run the script:
    ```bash
    python main.py
    ```

5. Enter the playlist ID when prompted, and the script will reorder the playlist for you.

## Usage

Once you've set up the `.env` file with your credentials and installed the required dependencies, run the script by executing:

```bash
python main.py
```

The script will prompt you to enter the Spotify playlist ID. After entering the playlist ID, it will reorder the tracks in the playlist based on the sorting logic (numbers first, then alphabetically).

## How it works

- The script uses the Spotify API to fetch all the tracks from the specified playlist.
- It sorts the tracks first by any numbers that appear at the beginning of the track name in ascending order, followed by alphabetical sorting for the rest.
- The playlist is then reordered with the sorted tracks on Spotify.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes. If you encounter any issues, please open an issue in the GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Spotipy](https://github.com/plamere/spotipy) for the Python client library to interact with Spotify's Web API.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for managing environment variables in a `.env` file.
