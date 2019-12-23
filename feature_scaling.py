import pandas as pd
import sqlite3
from sklearn.preprocessing import RobustScaler


"""
Connect to DB
Read in all data

"""
connection = sqlite3.connect('spotify_analysis_db')
cursor = connection.cursor()

# DB connect and fetch
get_all_query = "SELECT * from spotify_songs"

# Create Dataframe
df = pd.read_sql_query(get_all_query, connection)

columns = ['duration_ms', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

robust_scaler = RobustScaler()

df[columns] = robust_scaler.fit_transform(df[columns])

df.to_sql('spotify_songs_scaled', connection)
