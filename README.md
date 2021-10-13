# Billboard100-and-SpotifyAPI-SongFeatures-Scrape
Python script to scrape the Billboard Top 100 and search for the songs' features on Spotify through the Spotify API. Results are saved and exported in a pandas df.

Spotify has quantified a number of song characteristics ("song features") that could be useful for studying trends on song popularity. 

The script scrapes the weekly Billboard Top 100 songs based on a user-specified date range, and iterates through scraped song list, searching Spotify's API by artist and song name for the song's features. 

The resulting information is saved into a pandas df and exported. 

Notes on using:
- The user will first have to register with Spotify as a developer (this is free and takes about a minute). There are many tutorials online explaining the process. Once granted access, the user will be given a "Client ID" and "Client Secret. These must be entered in the script under the objects "client_id" and "client_secret". 
- The Billboard date range must be entered in the script
- Some songs (most likely those with a featured artist) have artist names displayed differently on Billboard and Spotify. These songs will not yield a song features result. I will include a script to manually search these songs. 


