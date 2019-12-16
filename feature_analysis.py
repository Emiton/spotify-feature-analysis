import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sqlite3


## Grab a given feature, but only a certain genre
# hip_energy = df['energy'][df['genre'] == 'Hip-Hop']

## Get unique values
# print(df.playlist.unique())


"""
TODO
Feature Selection



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



def features_dist_by_genre():
    """
    Create figures of feature with distribution by genre
    """
    for i in range(len(features)):
        plt.figure(i + 1)

        for genre in genres:
            genre_data = df[features[i]][df['genre'] == genre]
            sns.distplot(genre_data, hist=False, kde=True, kde_kws={'linewidth': 3}, label=genre)

        plt.title(f'{features[i]} by Genre')
        plt.xlabel(features[i])
        plt.show()
        # plt.savefig(f'./figures/{features[i]}_by_genre', bbox_inches='tight')


def correlation_matrix_by_genre():
    """
    Create a feature correlation matrix for each genre
    """
    for i in range(len(genres)):
        plt.figure(i + 1)
        plt.figure(figsize=(12, 10))
        genre_data = df[df['genre'] == genres[i]]
        correlation = genre_data.corr()
        sns.heatmap(correlation, annot=True, cmap=plt.cm.Reds)
        plt.title(f'Correlation Matrix: {genres[i]}')
        plt.show()


# correlation_matrix_by_genre()

genre_default_values = {
    'Hip-Hop': 1,
    'country': 2,
    'pop': 3,
    'rock': 4,
    'r&b': 5,
    'classical': 6,
    'electronic': 7
}


def feature_importance():
    """
    Use tree model to determine feature importance
    """
    df['new_genre'] = -1
    for i in range(len(genres)):
        df.loc[df['genre'] == genres[i], 'new_genre'] = genre_default_values[genres[i]]

    y = df.iloc[:, 17]
    x = df.iloc[:, 5:16]
    from sklearn.ensemble import ExtraTreesClassifier
    model = ExtraTreesClassifier()
    model.fit(x, y)
    print(model.feature_importances_)
    feat_importances = pd.Series(model.feature_importances_, index=x.columns)
    feat_importances.nlargest(10).plot(kind='barh')
    plt.show()


feature_importance()

