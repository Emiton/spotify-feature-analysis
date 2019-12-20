import pandas as pd
from pyclustering.cluster import cluster_visualizer_multidim
from pyclustering.cluster.cure import cure
from pyclustering.utils import read_sample
from pyclustering.samples.definitions import FCPS_SAMPLES
import sqlite3

connection = sqlite3.connect('spotify_analysis_db')
cursor = connection.cursor()

# DB connect and fetch
get_all_query = "SELECT * from spotify_songs"
cursor.execute(get_all_query)
rows = cursor.fetchall()

data = []

# Insert all values from sql query into 2D array
for row in rows:
    feature_values = []
    i = 4
    while i < len(row):
        feature_values.append(row[i])
        i += 1
    data.append(feature_values)


# Create Dataframe
df = pd.read_sql_query(get_all_query, connection)
input_data = x = df.iloc[:, 5:16]

# # Cluster
cure_instance = cure(data, 3)
cure_instance.process()
clusters = cure_instance.get_clusters()


print('About to visualize')
# Visualize clusters
visualizer = cluster_visualizer_multidim()
visualizer.append_clusters(clusters, data)
visualizer.show()

print('Done with visualization')
