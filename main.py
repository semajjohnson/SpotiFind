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
    scope="user-top-read user-read-recently-played"
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

#user profile data function
def fetch_my_user():
    try:
        user_data = sp.me()

        user_id = user_data.get('id', 'N/A')  # Fallback to 'N/A' if 'id' isn't present
        display_name = user_data.get('display_name', 'N/A')
        email = user_data.get('email', 'No email available')

        print(f"User ID: {user_id}")     
        print(f"Display Name: {display_name}")   
        print(f"Email: {email}")
    except Exception as e:
        print("An error occurred:", e)

def fetch_top_tracks(limit = 20):
    try:
        top_tracks = sp.current_user_top_tracks(limit=20, time_range="medium_term")
        print("Your Top Tracks:")
        for idx, item in enumerate(top_tracks['items']):
            print(f"{idx + 1}: {item['name']} by {item['artists'][0]['name']}")
        return top_tracks
    except Exception as e:
        print("An error occurred:", e)   

top_tracks = fetch_top_tracks() 

def fetch_top_artists():
    try:  
        top_artists = sp.current_user_top_artists(limit=10, time_range="medium_term")
        print("\n" + "Your Top Artist:")
        for idx, artist in enumerate(top_artists['items']):
            print(f"{idx + 1}: {artist['name']}")
        return top_artists
    except Exception as e:
        print("An error occurred:", e)
    
def fetch_recently_played():
    try:
        recently_played = sp.current_user_recently_played(limit=10)
        print("\n" + "Recently Played Tracks:")
        for idx, item in enumerate(recently_played['items']):
            track = item['track']
            print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']} (played at {item['played_at']})")
        return recently_played 
    except Exception as e:
        print("An error occurred:", e)

def fetch_top_genres():
    try:
        # Collect genres based on top tracks
        genres = set()  # using a set to avoid duplicates
        for track in top_tracks['items']:
            artist_id = track['artists'][0]['id']
            artist = sp.artist(artist_id)
            genres.update(artist['genres'])

        # Print unique genres
        print("Top Genres:")
        for genre in genres:
            print(genre)
    except Exception as e:
        print("An error occurred:", e)    

def get_user_data():
    try:
        # Fetch data
        top_tracks = fetch_top_tracks()
        top_artists = fetch_top_artists()
        recently_played = fetch_recently_played()
    except Exception as e:
        print("An error occurred:", e)
    
    # Structure data for SQL
    user_data = {
        "top_tracks": [(track['name'], track['artists'][0]['name']) for track in top_tracks['items']],
        "top_artists": [artist['name'] for artist in top_artists['items']],
        "recently_played": [(item['track']['name'], item['track']['artists'][0]['name'], item['played_at']) for item in recently_played['items']],
        "top_genres": [genre for artist in top_artists['items'] for genre in artist['genres']]
    }
    print("\n")
    return user_data       

# Run the test function
if __name__ == "__main__":
    user_data = get_user_data()
    print("User Data Retrieved:")
    print(user_data)

print("done") 
