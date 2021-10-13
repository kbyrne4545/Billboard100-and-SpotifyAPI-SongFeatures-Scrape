# This script can be used to search manually for songs that the larger script does not find a match for

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

client_id = 'xxxxx'
client_secret = 'xxxxx'
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

df.to_csv('song_features.csv')
















