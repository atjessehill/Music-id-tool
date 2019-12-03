import os, requests, json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from dotenv import load_dotenv
from time import sleep

load_dotenv()

client = os.getenv("SPOT_CLIENT")
secret = os.getenv("SPOT_SECRET")
username = os.getenv("SPOT_USERNAME")

uri = '5S6XqiyVSF0OU96LOw9UXP'

class current_song:
    def __init__(self, album=None, artist=None, song=None, bare_uri=None, album_art=None, full_uri=None, duration_left = None, duration_ms=None, popularity=None):
        self.name = song
        self.artist = artist
        self.album = album
        self.bare_uri = bare_uri
        self.full_uri = full_uri
        self.album_art = album_art
        self.duration_left = duration_left
        self.duration_ms = duration_ms
        self.popularity = popularity

    def print(self):

        print("SONG: ", self.name)
        print("ARTIST: ", self.artist)
        print("ALBUM: ", self.album)
        print("DURATION: ", self.duration_ms)
        print("POPULARITY: ", self.popularity)

def get_user_session_token():

    # sp = spotipy.Spotify(auth=username)

    scope = 'user-read-currently-playing'


    token = util.prompt_for_user_token(username=username, scope=scope, client_id=client,
                                       client_secret=secret, redirect_uri='http://localhost/')

    return token

def get_sp_client():

    client_credentials_manager = SpotifyClientCredentials(client_id=client, client_secret=secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return sp

def get_current_song():
    token = get_user_session_token()
    bearer = 'Bearer ' + token
    headers = {
        'Authorization': bearer
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    if response.status_code != 200:
        print("STATUS CODE WAS NOT 200:", response.status_code)
        return None
    elif response.status_code == 200:

        song_data = response.json()['item']
        progress_ms = response.json()['progress_ms']

        artist = []
        for a in song_data['artists']:
            artist.append(a['name'])

        artist = ",".join(artist)
        song = song_data['name']
        album = song_data['album']['name']

        uri = song_data['uri']
        album_art = song_data['album']['images']
        bare_uri = uri.split(':')[2]
        duration_ms = song_data['duration_ms']
        popularity = song_data['popularity']
        duration_left = duration_ms - progress_ms

        song = current_song(album, artist, song, bare_uri, album_art, uri, duration_left, duration_ms, popularity)
        return song


# analysis = sp.current_user_playing_track()

test_uri = '0QNkVh7nw7KkQSPkjharYW'
test_album = 'How The Dogs Chill, Vol. 1'
test_artist = 'Mall Grab'
test_artist = 'Liverpool Street In The Rain'

minute = 60000
sp = get_sp_client()
while(True):

    print("Calling get_current_song")
    song = get_current_song()
    if song == None:
        print("no song found")
        sleep(minute)
    else:
        song.print()
        analysis = sp.audio_features(uri)
        print(analysis)
        time_to_sleep = song.duration_left / 1000
        print("going to sleep ", time_to_sleep, '(seconds)')
        time_to_sleep += 10 # Buffer time to let the next song get a few seconds in
        sleep(time_to_sleep)
        print(analysis)

# get_current_song()


