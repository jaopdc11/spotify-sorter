# Spotify Playlist Organizer

This Python script allows you to reorder tracks in a Spotify playlist based on various sorting options. It uses the Spotify API to fetch the tracks and reorder them.

## Features

- Reorders tracks in a Spotify playlist.
- Sorting options:
  - Alphabetical order.
  - By artist name.
  - By album name.
- Uses the Spotify API for authentication and playlist management.
- Configuration settings are loaded from a `.env` file for security.

## Prerequisites

Before using the script, make sure you have:

- A Spotify developer account and an app to get your `CLIENT_ID` and `CLIENT_SECRET`.
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

5. Enter the playlist URL when prompted, and choose a sorting option to reorder the playlist.

## Usage

Once you've set up the `.env` file with your credentials and installed the required dependencies, run the script by executing:

```bash
python main.py
```

The script will prompt you to enter the Spotify playlist URL and select a sorting option. After entering the playlist details, it will reorder the tracks in the playlist accordingly.

## How it works

- The script uses the Spotify API to fetch all the tracks from the specified playlist.
- It sorts the tracks based on the selected sorting option.
- The playlist is then updated with the sorted tracks on Spotify.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes. If you encounter any issues, please open an issue in the GitHub repository.

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial (CC BY-NC)** license.

### Terms of Use

- You are free to:
  - Copy, modify, distribute, and perform the work for non-commercial purposes.
  
- You must, at a minimum, provide proper attribution to the author (me), including the name of the author and a link to the original project.

- You cannot:
  - Sell this software, or sell any derivative works based on it.
  - Use this software for commercial purposes.

For more information, visit: [Creative Commons License](https://creativecommons.org/licenses/by-nc/4.0/).

## Acknowledgements

- [Spotipy](https://github.com/plamere/spotipy) for the Python client library to interact with Spotify's Web API.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for managing environment variables in a `.env` file.
