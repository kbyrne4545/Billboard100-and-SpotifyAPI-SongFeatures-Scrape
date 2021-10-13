import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
from re import search
import requests
from bs4 import BeautifulSoup
import datetime


# Register with Spotify for client_id and client_secret
client_id = 'xxxxx'
client_secret = 'xxxxxx'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

#defining lists used to collect billboard website data
song_name = []
artist_name = []
song_rank = []
billboard_week = []

#defining lists used to collect spotify api data 
track_id_list = []
artist_name_list = []
track_name_list = []

#creating date variables 
#***CHANGE THESE IN CODE FOR DIFFERENT DATES***
start_date = datetime.date(2021,8,20)
end_date = datetime.date(2021,9,21)
dayit = int((end_date - start_date).days / 7)
day_delta = datetime.timedelta(days = 7)

for i in range(dayit + 1):
    
    #new search date for each loop
    search_date = start_date + i * day_delta
    
    #creates new df on each iteration
    df_BB = pd.DataFrame()
    
    URL_body = "https://www.billboard.com/charts/hot-100/"
    URL_date = str(search_date)
    
    response =requests.get(URL_body + URL_date)
    web_page = response.text
    
    soup = BeautifulSoup(web_page, "html.parser")
    
    titles = soup.find_all("span", class_="chart-element__information__song")
    artists = soup.find_all("span", class_="chart-element__information__artist")
    ranks = soup.find_all("span", class_="chart-element__rank__number")
    
    #saves elements to lists
    for song in titles:
        song_name.append(song.getText())
    
    for name in artists:
        artist_name.append(name.getText())
    
    for number in ranks:
        song_rank.append(number.getText())
    
    for i in range(100):
        billboard_week.append(search_date)
    
    #places lists into df
    df_BB['Date'] = billboard_week
    df_BB['Rank'] = song_rank
    df_BB['Artist'] = artist_name
    df_BB['Song'] = song_name


for n in range(len(df_BB) // 100):
    for r in range(99):
        artist = df_BB.iloc[r+(n*100),2]
        track = df_BB.iloc[r+(n*100),3]
    
        try:
            spotify_response = sp.search(q='artist:' + artist + ' track:' + track, type='track')           
            artist_name = spotify_response['tracks']['items'][0]['artists'][0]['name']
            track_name = spotify_response['tracks']['items'][0]['name']
            #unique spotify track id used for audio feature search
            track_id = spotify_response['tracks']['items'][0]['uri']           
            #splits string to search for features
            track_id_split = str.split(track_id, 'spotify:track:')
            track_id_list.append(track_id_split[1])          
            artist_name_list.append(artist)          
            track_name_list.append(track)
            
        except:
            DNF_song_search = sp.search(q=track)
            artist_name = DNF_song_search['tracks']['items'][0]['artists'][0]['name']
            
            if search(artist_name, artist):     
                track_name = DNF_song_search['tracks']['items'][0]['name']
                track_id = DNF_song_search['tracks']['items'][0]['uri']
                track_id_split = str.split(track_id, 'spotify:track:')
                track_id_list.append(track_id_split[1])
                artist_name_list.append(artist)
                track_name_list.append(track)
                
            else:
                print('Inconsistent artist match on: ' + artist + ' ' + artist_name + ' for song ' + track)

features_df = pd.DataFrame()
for num in range(len(track_id_list) // 100 + 1):
    features = sp.audio_features(track_id_list[(num*100):(num+1)*100])
    features_df = features_df.append(pd.DataFrame(features))

#add artist and song columns from imported billboard df
features_df['Artist'] = artist_name_list
features_df['Song'] = track_name_list

#combine the two dataframes
df_merged = pd.merge(df_BB, features_df.drop_duplicates(), on = 'Song', how = 'left')

df_merged.to_csv('mergedv2.csv')








    
    
    
    
    








