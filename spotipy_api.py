import json # TODO: Remove
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials # For Spotify API use

username = 'Emiton Alves'
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
all_playlists = {}

# TODO: See if redirect is necessary
# redirect_uri = 'http://localhost/5000'
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():
    playlists_to_analyze = [
        'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd',
    ]

    for playlist in playlists_to_analyze:
        get_playlist_audio_features(playlist)

    visualize_playlist_data(all_playlists['RapCaviar'])



def get_playlist_audio_features(uri):
    playlist_id = uri.split(':')[2]

    results = sp.user_playlist(user=username, playlist_id=playlist_id)


    playlist_name = results['name']

    all_playlists[playlist_name] = {}
    # all_playlists[playlist_name]['name'] = []
    # all_playlists[playlist_name]['track uri'] = []
    all_playlists[playlist_name]['acousticness'] = []
    all_playlists[playlist_name]['danceability'] = []
    all_playlists[playlist_name]['energy'] = []
    all_playlists[playlist_name]['instrumentalness'] = []
    all_playlists[playlist_name]['liveness'] = []
    all_playlists[playlist_name]['loudness'] = []
    all_playlists[playlist_name]['speechiness'] = []
    # all_playlists[playlist_name]['tempo'] = []
    all_playlists[playlist_name]['valence'] = []
    # TODO: Add popularity later
    # all_playlists[playlist_name]['popularity'] = []

    for track_metadata in results['tracks']['items']:
        # DEBUG STATEMENT
        # print(json.dumps(track, indent=4))

        if track_metadata['track'] is not None:
            # save metadata stuff
            name = track_metadata['track']['name']
            print(name)
            track_uri = track_metadata['track']['uri']
            # all_playlists[playlist_name]['name'].append(name)
            # all_playlists[playlist_name]['track uri'].append(track_uri)

            # extract features
            features = sp.audio_features(track_uri)
            all_playlists[playlist_name]['acousticness'].append(features[0]['acousticness'])
            all_playlists[playlist_name]['danceability'].append(features[0]['danceability'])
            all_playlists[playlist_name]['energy'].append(features[0]['energy'])
            all_playlists[playlist_name]['instrumentalness'].append(features[0]['instrumentalness'])
            all_playlists[playlist_name]['liveness'].append(features[0]['liveness'])
            all_playlists[playlist_name]['loudness'].append(features[0]['loudness'])
            all_playlists[playlist_name]['speechiness'].append(features[0]['speechiness'])
            # all_playlists[playlist_name]['tempo'].append(features[0]['tempo'])
            all_playlists[playlist_name]['valence'].append(features[0]['valence'])

    return results


def visualize_playlist_data(playlist):
    # create dataframe
    df = pd.DataFrame.from_dict(playlist)
    fig = plt.figure()

    # sns.distplot(df['acousticness'], hist='true', kde='false', bins=25)
    # sns.distplot(df['danceability'], hist='true', kde='false', bins=25)
    # sns.distplot(df['energy'], hist='true', kde='false', bins=25)
    # sns.distplot(df['instrumentalness'], hist='true', kde='false', bins=25)
    # sns.distplot(df['liveness'], hist='true', kde='false', bins=25)
    # sns.distplot(df['loudness'], hist='true', kde='false', bins=25)
    # sns.distplot(df['speechiness'], hist='true', kde='false', bins=25)
    # sns.distplot(df['tempo'], hist='true', kde='false', bins=25)
    # sns.distplot(df['valence'], hist='true', kde='false', bins=25)

    df.boxplot()

    plt.show()
    return ""


if __name__ == '__main__':
        main()
