from itertools import combinations
from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster import cluster_visualizer_multidim
from pyclustering.cluster.cure import cure
import statistics as stats
import sqlite3


def cluster_data(data, cluster_size):
    cure_instance = cure(data, cluster_size)
    cure_instance.process()
    clusters = cure_instance.get_clusters()
    # print(f'CLUSTERS:\n{clusters}')
    return clusters


def visualize_clusters(clusters, data):
    print('About to visualize')
    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, data)
    visualizer.show()
    print('Done with visualization')


# 7 for the 7 main genres represented
def get_top_clusters(clusters, count=7):
    sorted_groups = sorted(clusters, key=len, reverse=True)
    top_clusters = []
    for j in range(count):
        top_clusters.append(sorted_groups[j])
    return top_clusters


def count_genre_occurrences(cluster):
    genre_occurrences = {}
    genre_occurrences['total'] = 0
    for song in cluster:
        genre = rows[song][3]

        if genre in genre_occurrences:
            genre_occurrences[genre] += 1
            genre_occurrences['total'] += 1

        else:
            genre_occurrences[genre] = 1
            genre_occurrences['total'] += 1

    return genre_occurrences


def find_highest_genre_percentage(genre_occurrences):
    most_common = 0

    for key in genre_occurrences:
        if key is not 'total':
            most_common = max(most_common, genre_occurrences[key])
    return most_common / genre_occurrences['total']


def cluster_statistics(cluster_genre_count):
    percentages = []
    for count in cluster_genre_count:
        percentages.append(count[1])
    mean = stats.mean(percentages)
    median = stats.median(percentages)
    stdev = stats.stdev(percentages)
    # print(f'MEAN: {mean}')
    # print(f'MEDIAN: {median}')
    # print(f'STD DEV: {stdev}')

    return mean, median, stdev


connection = sqlite3.connect('spotify_analysis_db')
cursor = connection.cursor()

# DB connect and fetch
get_all_query = "SELECT * from spotify_songs_scaled"
cursor.execute(get_all_query)
rows = cursor.fetchall()

input_data = []

# Insert all values from sql query into 2D array
for row in rows:
    feature_values = []
    i = 8
    while i < len(row):
        if 8 <= i <= 10:
            feature_values.append(row[i])
        i += 1
    input_data.append(feature_values)

groups = cluster_data(input_data, 75)
# visualize_clusters(groups, input_data)


def cluster_all_possible_combinations(feature_set_count, cluster_size):
    features = [9, 10, 11, 12, 13, 14, 15, 16, 17]

    # Cluster all combinations
    possible_combinations = combinations(features, feature_set_count)

    average_mean = []
    average_median = []
    average_stdev = []
    for combo in possible_combinations:
        # print(f'COMBO: {combo}')

        # Create reduced data set
        curr_data = []
        for row in rows:
            feature_list = []
            for index in combo:
                feature_list.append(row[index])
            curr_data.append(feature_list)

        # Cluster reduced data
        all_clusters = cluster_data(curr_data, cluster_size)

        top_clusters = get_top_clusters(all_clusters)

        all_clusters_genre_count = []
        for clust in top_clusters:
            genre_count = count_genre_occurrences(clust)
            genre_top_percentage = find_highest_genre_percentage(genre_count)
            all_clusters_genre_count.append((genre_count, genre_top_percentage))
        all_clusters_genre_count.sort(key=lambda x: x[1], reverse=True)
        average_mean.append(cluster_statistics(all_clusters_genre_count)[0])
        average_median.append(cluster_statistics(all_clusters_genre_count)[1])
        average_stdev.append(cluster_statistics(all_clusters_genre_count)[2])

    file = open("scaled_tests.txt", "a+")
    file.write(f'RESULTS FOR -- Count: {feature_set_count}  , Cluster Size: {cluster_size}\n')
    file.write(f'\tAverage mean: {stats.mean(average_mean)}\n')
    file.write(f'\tAverage median: {stats.mean(average_median)}\n')
    file.write(f'\tAverage standard deviation: {stats.mean(average_stdev)}\n')
    file.close()

    print(f'RESULTS FOR -- Count: {feature_set_count}  , Cluster Size: {cluster_size}')
    print(f'\tAverage mean: {stats.mean(average_mean)}')
    print(f'\tAverage median: {stats.mean(average_median)}')
    print(f'\tAverage standard deviation: {stats.mean(average_stdev)}')


# cluster_all_possible_combinations(2, 25)

cluster_sizes = [7, 25, 75, 100, 150, 200, 250]

for size in cluster_sizes:
    for i in range(2, 10):
        cluster_all_possible_combinations(i, size)
