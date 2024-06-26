import os
import pandas as pd
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


def extract_spotify():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    latam_country_list = ['Peru', 'Chile', 'Argentina', 'Colombia', 'Mexico', 'Ecuador', 'Bolivia', 'Paraguay',
                          'Uruguay', 'Venezuela', 'Brazil']

    top_50 = sp.search(q='Top 50 - ', type='playlist', limit=50, market='PE')

    playlists = top_50['playlists']['items']

    listas = {}
    for playlist in playlists:
        name = playlist['name']
        id_playlist = playlist['id']
        for country in latam_country_list:
            if name.startswith('Top 50 - ') and name.endswith(country):
                top50_country = sp.playlist_tracks(id_playlist)
                listas[country] = []
                for i, top50 in enumerate(top50_country['items']):
                    preview = top50['track']['preview_url']
                    song = top50['track']['name']
                    artists = [artist['name'] for artist in top50['track']['artists']]
                    artists = ', '.join(artists)
                    albums = top50['track']['album']['name']
                    release_date = top50['track']['album']['release_date']
                    popularity = top50['track']['popularity']
                    listas[country].append(
                        {'ranking': i + 1, 'song': song, 'artists': artists, 'albums': albums, 'popularity': popularity,
                         'release_date': release_date, 'preview': preview})

    dataframes = [pd.DataFrame(listas[country]) for country in listas]
    df = pd.concat(dataframes, keys=listas.keys())
    df_reset = df.reset_index()
    df_reset = df_reset.drop('level_1', axis=1)
    df_reset.rename(columns={'level_0': 'country'}, inplace=True)
    return df_reset


def unique_country():
    df = extract_spotify()
    countries = df['country'].unique().tolist()
    return countries
