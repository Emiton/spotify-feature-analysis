import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials  # For Spotify API use
import sqlite3

username = 'Emiton Alves'
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
all_playlists = {}

# Might need redirect if trouble hosting locally
# redirect_uri = 'http://localhost/5000'
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

connection = sqlite3.connect('spotify_analysis_db')
cursor = connection.cursor()
query_string = (
    "CREATE TABLE IF NOT EXISTS spotify_songs ("
    "track_uri TEXT NOT NULL, "
    "name TEXT, "
    "genre TEXT, "
    "playlist TEXT, "
    "duration_ms INTEGER, "
    "key INTEGER, "
    "mode INTEGER, "
    "time_signature INTEGER, "
    "acousticness REAL, "
    "danceability REAL, "
    "energy REAL, "
    "instrumentalness REAL, "
    "liveness REAL, "
    "loudness REAL, "
    "speechiness REAL, "
    "tempo REAL, "
    "valence REAL, "
    " PRIMARY KEY (track_uri))"
)
cursor.execute(query_string)


def main():
    with open('playlists_to_work_with.json') as json_file:
        playlists_to_work_with = json.load(json_file)

    for genre in playlists_to_work_with:
        for plist in playlists_to_work_with[genre]:
            get_playlist_audio_features(plist[0], plist[1], genre)

    cursor.close()
    connection.close()

    # manually inspect all of the values to determine whether the median or mean is a better metric to plot
    for playlist1 in all_playlists:
        print("–" * 70)
        print(playlist1)
        for feature in all_playlists[playlist1]:
            if feature != 'name' and feature != 'track uri' and feature != 'playlist' and feature != 'genre' and feature != 'track uri':
                print(feature.upper(),
                      "| median:", np.median(all_playlists[playlist1][feature]),
                      "| mean:", np.mean(all_playlists[playlist1][feature]))

    labels = ['acousticness', 'danceability', 'energy', 'valence', 'instrumentalness', 'tempo', 'speechiness']
    num_vars = len(labels)

    # Split the circle into even parts and save the angles so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # ax = plt.subplot(polar=True)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Helper function to plot each playlist on the radar chart.
    def add_to_radar(playlist, color):
        values = [np.median(all_playlists[playlist]['acousticness']), np.median(all_playlists[playlist]['danceability']),
                  np.median(all_playlists[playlist]['energy']),
                  np.median(all_playlists[playlist]['valence']), np.mean(all_playlists[playlist]['instrumentalness']),
                  np.median(all_playlists[playlist]['tempo']),
                  np.median(all_playlists[playlist]['speechiness'])]
        # tempo values typically range from 50-220 --> squash range to 0-1
        values[-2] = values[-2] / 220
        # speechiness values values are highly concentrated between 0 and 0.25-ish --> expand range to 0-1
        values[-1] = values[-1] * 4
        values += values[:1]
        ax.plot(angles, values, color=color, linewidth=1, label=playlist)
        ax.fill(angles, values, color=color, alpha=0.25)

    # Add each additional playlist to the chart.
    add_to_radar('RapCaviar', 'red')
    add_to_radar('Hot Country', 'green')
    add_to_radar('Morning Classical', 'blue')

    # polar coordinates math for radar graph
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles), labels)

    # Go through labels and adjust alignment based on where it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Set position of y-labels (0-100) to be in the middle of the first two axes.
    ax.set_ylim(0, 1)
    ax.set_rlabel_position(180 / num_vars)

    # Add some custom styling.
    ax.tick_params(colors='#222222')  # color of tick labels
    ax.tick_params(axis='y', labelsize=8)  # y-axis labels
    ax.grid(color='#AAAAAA')  # color of circular gridlines
    ax.spines['polar'].set_color('#222222')  # color of outermost gridline (spine)
    ax.set_facecolor('#FAFAFA')  # background color inside the circle itself

    # Give the chart a title and a legend
    ax.set_title('Playlist Comparison', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    fig.savefig('playlist_comp.png')
    plt.show()


def get_playlist_audio_features(playlist, uri, genre):
    playlist_id = uri.split(':')[2]

    results = sp.user_playlist(user=username, playlist_id=playlist_id)

    playlist_name = results['name']
    all_playlists[playlist_name] = {}
    all_playlists[playlist_name]['track uri'] = []
    all_playlists[playlist_name]['name'] = []
    all_playlists[playlist_name]['genre'] = []
    all_playlists[playlist_name]['playlist'] = []
    all_playlists[playlist_name]['duration_ms'] = []
    all_playlists[playlist_name]['key'] = []
    all_playlists[playlist_name]['mode'] = []
    all_playlists[playlist_name]['time_signature'] = []
    all_playlists[playlist_name]['acousticness'] = []
    all_playlists[playlist_name]['danceability'] = []
    all_playlists[playlist_name]['energy'] = []
    all_playlists[playlist_name]['instrumentalness'] = []
    all_playlists[playlist_name]['liveness'] = []
    all_playlists[playlist_name]['loudness'] = []
    all_playlists[playlist_name]['speechiness'] = []
    all_playlists[playlist_name]['tempo'] = []
    all_playlists[playlist_name]['valence'] = []

    for track_metadata in results['tracks']['items']:
        # DEBUG STATEMENT
        # print(json.dumps(track, indent=4))

        if track_metadata['track'] is not None:
            # save metadata
            name = track_metadata['track']['name']
            print(name)
            track_uri = track_metadata['track']['uri']
            all_playlists[playlist_name]['track uri'].append(track_uri)
            all_playlists[playlist_name]['name'].append(name)
            all_playlists[playlist_name]['genre'].append(genre)
            all_playlists[playlist_name]['playlist'].append(playlist)

            # extract features
            features = sp.audio_features(track_uri)
            if features != [None]:
                all_playlists[playlist_name]['duration_ms'].append(features[0]['duration_ms'])
                all_playlists[playlist_name]['key'].append(features[0]['key'])
                all_playlists[playlist_name]['mode'].append(features[0]['mode'])
                all_playlists[playlist_name]['time_signature'].append(features[0]['time_signature'])
                all_playlists[playlist_name]['acousticness'].append(features[0]['acousticness'])
                all_playlists[playlist_name]['danceability'].append(features[0]['danceability'])
                all_playlists[playlist_name]['energy'].append(features[0]['energy'])
                all_playlists[playlist_name]['instrumentalness'].append(features[0]['instrumentalness'])
                all_playlists[playlist_name]['liveness'].append(features[0]['liveness'])
                all_playlists[playlist_name]['loudness'].append(features[0]['loudness'])
                all_playlists[playlist_name]['speechiness'].append(features[0]['speechiness'])
                all_playlists[playlist_name]['tempo'].append(features[0]['tempo'])
                all_playlists[playlist_name]['valence'].append(features[0]['valence'])

                query = (
                    "INSERT OR REPLACE INTO spotify_songs ("
                    "track_uri, name, genre, playlist, duration_ms, key, mode, time_signature, "
                    "acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, "
                    "tempo, valence) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                )

                cursor.execute(
                    query,
                    (
                        track_uri,
                        name,
                        genre,
                        playlist,
                        features[0]['duration_ms'],
                        features[0]['key'],
                        features[0]['mode'],
                        features[0]['time_signature'],
                        features[0]['acousticness'],
                        features[0]['danceability'],
                        features[0]['energy'],
                        features[0]['instrumentalness'],
                        features[0]['liveness'],
                        features[0]['loudness'],
                        features[0]['speechiness'],
                        features[0]['tempo'],
                        features[0]['valence']
                    )
                )

                connection.commit()

    return results


def visualize_playlist_data(playlist):
    df = pd.DataFrame.from_dict(playlist) # wont work if name and track_uri are in df
    df.boxplot()
    plt.show()


if __name__ == '__main__':
        main()
