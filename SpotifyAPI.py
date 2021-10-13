# Interacting with the Spotify API
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

client_id = '344e801b609e4a82912c8942de5c543b'
client_secret = '6dde89705ad642e9a83c828e0685135e'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

artist = 'Meek Mill'
track = 'Blue Note'

spotify_response = sp.search(q='artist:' + artist + ' track:' + track, type='track')

#artist name
artist_name = spotify_response['tracks']['items'][0]['artists'][0]['name']

#song name
track_name = spotify_response['tracks']['items'][0]['name']

#unique sportify track id used for audio feautre search
track_id = spotify_response['tracks']['items'][0]['uri']

#splits string to search for features
track_id_split = str.split(track_id, 'spotify:track:')

features = sp.audio_features(track_id_split[1])

print(features)

df = pd.DataFrame(features)
df.insert(0,'Artist', artist_name)
df.insert(1,'Song Name', track_name)

display(df)

df.to_csv('samples.csv')
















