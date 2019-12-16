import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sqlite3


"""
TODO




DONE 
    Get all data from sqlite DB
    Create DataFrame
    Create feature distributions for each genre on same chart
"""


connection = sqlite3.connect('spotify_analysis_db')
cursor = connection.cursor()

genres = ['Hip-Hop', 'country', 'pop', 'rock', 'r&b', 'classical', 'electronic']
features = [
    'duration_ms', 'key', 'mode', 'time_signature', 'acousticness',
    'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
]

# DB connect and fetch
get_all_query = "SELECT * from spotify_songs"
cursor.execute(get_all_query)
rows = cursor.fetchall()

# Create Dataframe
df = pd.read_sql_query(get_all_query, connection)

# print(df.playlist.unique())

# Create figures of feature with dist per genre
for i in range(len(features) - 1):
    plt.figure(i + 1)

    for genre in genres:
        genre_type = df[features[i]][df['genre'] == genre]
        sns.distplot(genre_type, hist=False, kde=True, kde_kws={'linewidth': 3}, label=genre)

    plt.title(f'{features[i]} by Genre')
    plt.xlabel(features[i])
    plt.show()
    plt.savefig(f'./figures/{features[i]}_by_genre', bbox_inches='tight')

# Grab a given feature, but only a certain genre
# hip_energy = df['energy'][df['genre'] == 'Hip-Hop']



"""
Compute per playlist for a feature by genre
    
    Get column
    Determine all possible values for column
    use values to do same calculation but for playlist
"""

