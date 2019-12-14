import json # TODO: Remove
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials  # For Spotify API use

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

    plists_to_work_with = {
        'Hip-Hop': [
            ('RapCaviar', 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'),
            ('Get Turnt', 'spotify:playlist:37i9dQZF1DWY4xHQp97fN6'),
            ('Feelin\' Myself', 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq'),
            ('Most Necessary', 'spotify:playlist:37i9dQZF1DX2RxBh64BHjQ'),
            ('I Love My \'90s Hip-Hop', 'spotify:playlist:37i9dQZF1DX186v583rmzp'),
            ('Signed XOXO', 'spotify:playlist:37i9dQZF1DX2A29LI7xHn1'),
            ('Gold School', 'spotify:playlist:37i9dQZF1DWVA1Gq4XHa6U'),
            ('If It Wasn\'t For Gucci', 'spotify:playlist:37i9dQZF1DXcWxeqLvgOCi'),
            ('Grime Shutdown', 'spotify:playlist:37i9dQZF1DWSOkubnsDCSS'),
            ('This Is A$AP Mob', 'spotify:playlist:37i9dQZF1DWXmxXDRgAKVq'),
        ],
        'country': [
            ('Hot Country', 'spotify:playlist:37i9dQZF1DX1lVhptIYRda'),
            ('Country Kind Of Love', 'spotify:playlist:37i9dQZF1DX8WMG8VPSOJC'),
            ('Chillin\' on a Dirt Road', 'spotify:playlist:37i9dQZF1DWTkxQvqMy4WW'),
            ('Country Gold', 'spotify:playlist:37i9dQZF1DWYnwbYQ5HnZU'),
            ('Wild Country', 'spotify:playlist:37i9dQZF1DX5mB2C8gBeUM'),
            ('Country by the Grace of God', 'spotify:playlist:37i9dQZF1DWU2LcZVHsTdv'),
            ('Country Nights', 'spotify:playlist:37i9dQZF1DWXi7h4mmmkzD'),
            ('Drunk and Hungover', 'spotify:playlist:37i9dQZF1DX3ph0alWhOXm'),
            ('Country Music 101: Country\'s Greatest Hits','spotify:playlist:37i9dQZF1DWZBCPUIUs2iR'),
            ('New Boots', 'spotify:playlist:37i9dQZF1DX8S0uQvJ4gaa'),

        ],
        'pop': [
            ('Today\'s Top Hits', 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'),
            ('Pop Rising', 'spotify:playlist:37i9dQZF1DWUa8ZRTfalHk'),
            ('Hit Rewind', 'spotify:playlist:37i9dQZF1DX0s5kDXi1oC5'),
            ('Everyday Favorites', 'spotify:playlist:37i9dQZF1DX0MLFaUdXnjA'),
            ('Pop Party', 'spotify:playlist:37i9dQZF1DWXti3N4Wp5xy'),
            ('Indie Pop', 'spotify:playlist:37i9dQZF1DWWEcRhUVtL8n'),
            ('Sad Bops', 'spotify:playlist:37i9dQZF1DWZUAeYvs88zc'),
            ('Women of Pop','spotify:playlist:37i9dQZF1DX3WvGXE8FqYX'),
            ('Bedroom Pop', 'spotify:playlist:37i9dQZF1DXcxvFzl58uP7'),
            ('Fresh & Chill', 'spotify:playlist:37i9dQZF1DX5CdVP4rz81C'),

        ],
        'rock': [
            ('Rock Classics', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U'),
            ('90s Rock Anthems', 'spotify:playlist:37i9dQZF1DX1rVvRgjX59F'),
            ('00s Rock Anthems', 'spotify:playlist:37i9dQZF1DX3oM43CtKnRV'),
            ('80s Rock Anthems', 'spotify:playlist:37i9dQZF1DX1spT6G94GFC'),
            ('New Noise', 'spotify:playlist:37i9dQZF1DWT2jS7NwYPVI'),
            ('Rock This', 'spotify:playlist:37i9dQZF1DXcF6B6QPhFDv'),
            ('Rock Hard', 'spotify:playlist:37i9dQZF1DWWJOmJ7nRx0C'),
            ('Pure Rock & Roll', 'spotify:playlist:37i9dQZF1DWWRktbhJiuqL'),
            ('Rock Party', 'spotify:playlist:37i9dQZF1DX8FwnYE6PRvL'),
            ('Emo Forever', 'spotify:playlist:37i9dQZF1DX9wa6XirBPv8'),

        ],
        'r&b': [
            ('Are & Be', 'spotify:playlist:37i9dQZF1DX4SBhb3fqCJd'),
            ('I Love My 2000s R&B', 'spotify:playlist:37i9dQZF1DWYmmr74INQlb'),
            ('Black Girl Magic', 'spotify:playlist:37i9dQZF1DX4ezQVslkJiT'),
            ('I Love my \'90s R&B', 'spotify:playlist:37i9dQZF1DX6VDO8a6cQME'),
            ('Chilled R&B', 'spotify:playlist:37i9dQZF1DX2UgsUIg75Vg'),
            ('\'80s Jam Session', 'spotify:playlist:37i9dQZF1DX0H8hDpv38Ju'),
            ('The Newness', 'spotify:playlist:37i9dQZF1DWUzFXarNiofw'),
            ('The Cookout', 'spotify:playlist:37i9dQZF1DXab8DipvnuNU'),
            ('Fancy Friday', 'spotify:playlist:37i9dQZF1DWUbo613Z2iWO'),
            ('Queen', 'spotify:playlist:37i9dQZF1DWSIO2QWRavWZ'),

        ],
        'classical': [
            ('Classical Essentials', 'spotify:playlist:37i9dQZF1DWWEJlAGA9gs0'),
            ('Morning Classical', 'spotify:playlist:37i9dQZF1DX9OZisIoJQhG'),
            ('Chilled Classical', 'spotify:playlist:37i9dQZF1DWUvHZA1zLcjW'),
            ('Classical Sleep', 'spotify:playlist:37i9dQZF1DX8Sz1gsYZdwj'),
            ('Easy Classical', 'spotify:playlist:37i9dQZF1DX0Aaer4Jzfgm'),
            ('Epic Classical', 'spotify:playlist:37i9dQZF1DX9G9wwzwWL2k'),
            ('Classical Romance', 'spotify:playlist:37i9dQZF1DX4s3V2rTswzO'),
            ('Orchestra 100: Spotify Picks', 'spotify:playlist:37i9dQZF1DXddGd6mP5X2a'),
            ('Piano 100: Spotify Picks', 'spotify:playlist:37i9dQZF1DXah8e1pvF5oE'),
            ('Baroque 50: Spotify Picks', 'spotify:playlist:37i9dQZF1DWXjj6kdiviS0'),

        ],
        'electronic': [
            ('mint', 'spotify:playlist:37i9dQZF1DX4dyzvuaRJ0n'),
            ('Housewerk', 'spotify:playlist:37i9dQZF1DXa8NOEUWPn9W'),
            ('Dance Party', 'spotify:playlist:37i9dQZF1DXaXB8fQg7xif'),
            ('Dance Hits', 'spotify:playlist:37i9dQZF1DX0BcQWzuB7ZO'),
            ('Night Rider', 'spotify:playlist:37i9dQZF1DX6GJXiuZRisr'),
            ('Rage Beats', 'spotify:playlist:37i9dQZF1DX3ND264N08pv'),
            ('Techno Bunker', 'spotify:playlist:37i9dQZF1DX6J5NfMJS675'),
            ('Shuffle Syndrome', 'spotify:playlist:37i9dQZF1DWUq3wF0JVtEy'),
            ('Trance Mission', 'spotify:playlist:37i9dQZF1DX91oIci4su1D'),
            ('Main Stage', 'spotify:playlist:37i9dQZF1DX7ZUug1ANKRP'),

        ],
    }
    playlists_to_analyze = [
        'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd',
        'spotify:playlist:37i9dQZF1DX1lVhptIYRda',
        'spotify:playlist:37i9dQZF1DX9OZisIoJQhG',
    ]

    # for plist in playlists_to_analyze:
    #     get_playlist_audio_features(plist)

    for genre in plists_to_work_with:
        for playlist in plists_to_work_with[genre]:
            get_playlist_audio_features(playlist[0], playlist[1], genre)

    # visualize_playlist_data(all_playlists['RapCaviar'])

    # manually inspect all of the values to determine whether the median or mean is a better metric to plot
    for playlist1 in all_playlists:
        print("–" * 70)
        print(playlist1)
        for feature in all_playlists[playlist1]:
            if feature != 'name' and feature != 'track uri':
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

    # polar coordinates math stuff
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

    # Lastly, give the chart a title and a legend
    ax.set_title('Playlist Comparison', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    fig.savefig('playlist_comp.png')
    plt.show()


def get_playlist_audio_features(playlist, uri, genre):
    playlist_id = uri.split(':')[2]

    results = sp.user_playlist(user=username, playlist_id=playlist_id)

    playlist_name = results['name']
    all_playlists[playlist_name] = {}
    all_playlists[playlist_name]['name'] = []
    all_playlists[playlist_name]['genre'] = []
    all_playlists[playlist_name]['playlist'] = []
    all_playlists[playlist_name]['track uri'] = []
    all_playlists[playlist_name]['acousticness'] = []
    all_playlists[playlist_name]['danceability'] = []
    all_playlists[playlist_name]['energy'] = []
    all_playlists[playlist_name]['instrumentalness'] = []
    all_playlists[playlist_name]['liveness'] = []
    all_playlists[playlist_name]['loudness'] = []
    all_playlists[playlist_name]['speechiness'] = []
    all_playlists[playlist_name]['tempo'] = []
    all_playlists[playlist_name]['valence'] = []
    all_playlists[playlist_name]['popularity'] = []

    for track_metadata in results['tracks']['items']:
        # DEBUG STATEMENT
        # print(json.dumps(track, indent=4))

        if track_metadata['track'] is not None:
            # save metadata stuff
            name = track_metadata['track']['name']
            print(name)
            track_uri = track_metadata['track']['uri']
            all_playlists[playlist_name]['name'].append(name)
            all_playlists[playlist_name]['genre'].append(genre)
            all_playlists[playlist_name]['playlist'].append(playlist)
            all_playlists[playlist_name]['track uri'].append(track_uri)

            # extract features
            features = sp.audio_features(track_uri)
            if features != [None]:
                all_playlists[playlist_name]['acousticness'].append(features[0]['acousticness'])
                all_playlists[playlist_name]['danceability'].append(features[0]['danceability'])
                all_playlists[playlist_name]['energy'].append(features[0]['energy'])
                all_playlists[playlist_name]['instrumentalness'].append(features[0]['instrumentalness'])
                all_playlists[playlist_name]['liveness'].append(features[0]['liveness'])
                all_playlists[playlist_name]['loudness'].append(features[0]['loudness'])
                all_playlists[playlist_name]['speechiness'].append(features[0]['speechiness'])
                all_playlists[playlist_name]['tempo'].append(features[0]['tempo'])
                all_playlists[playlist_name]['valence'].append(features[0]['valence'])

    return results


def visualize_playlist_data(playlist):
    # create dataframe
    df = pd.DataFrame.from_dict(playlist) # wont work if name and track_uri are in df
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
