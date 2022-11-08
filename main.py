from pprint import pprint
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Setting fixed variables

date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')
URL = f'https://www.billboard.com/charts/hot-100/{date}/'
CID = os.environ['CID']
CS = os.environ['CS']
RURL = 'http://example.com'
UID = os.environ['UID']

# Launching website for webscraper
response = requests.get(url=URL)
top_100_html = response.text
soup = BeautifulSoup(top_100_html, 'html.parser')
top_100 = soup.select('li h3', class_='c-title')

# Cleaning data gotten from webscrapper

songs = []
for song in top_100:
    songs.append(song.getText().replace('\n', '').replace('\t', ''))
songs = songs[:100]

# accessing spotify API

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CID,
                                               client_secret=CS,
                                               redirect_uri=RURL,
                                               scope='playlist-modify-private',
                                               show_dialog=True,
                                               cache_path='token.txt'))

# Setting spotify API fixed variables

user_id = sp.current_user()["id"]
song_URI = []
year = date.split('-')[0]
not_available = 0

# Converting song name to Spotify code[URI]

for song in songs:
    results = sp.search(q=f'track:{song} year:{year}', type='track')
    try:
        uri = results['tracks']['items'][3]['id']
        song_URI.append(uri)
    except IndexError:
        print(f'{song} is not available on spotify')
        not_available += 1
print(f'There are {not_available} total song(s) that are not available')

# Creating New Playlist

create_playlist = sp.user_playlist_create(user=UID,
                                          name=f'Songs popular on {date}',
                                          public=False,
                                          collaborative=False,
                                          description=f'Made this playlist for you for the songs popping on {date}')
play_id = create_playlist['id']

# Adding list of names to created playlist

sp.playlist_add_items(playlist_id=play_id, items=song_URI)

