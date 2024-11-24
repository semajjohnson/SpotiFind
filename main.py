import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#load environment variables
load_dotenv()

#authenticate app with spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),  # Retrieved from your .env file
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="http://localhost:8888/callback",  # Must match your Spotify app settings
    scope="playlist-read-private playlist-read-collaborative playlist-modify-public "
          "playlist-modify-private user-library-read user-read-recently-played user-top-read"
))
# Test API Call: Fetch the current user's playlists
def fetch_playlists():
    try:
        playlists = sp.current_user_playlists()
        print("Your Playlists:")
        for playlist in playlists['items']:
            print(f"- {playlist['name']} (Tracks: {playlist['tracks']['total']})")
    except Exception as e:
        print(f"Error: {e}")

# Run the test function
if __name__ == "__main__":
    fetch_playlists()

print("done")    