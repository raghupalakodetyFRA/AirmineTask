import argparse
import pandas as pd
import random
from math import radians, degrees, sin, cos, asin, acos, sqrt
import numpy as np
try:
    from itertools import izip as zip
except ImportError:
    pass

def great_circle(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )


def print_result(df):
    global index, row, average_dist, df_closest
    for index, row in df.iterrows():
        print(row['city1'], row['city2'], str(row['distance']) + "Km")
    average_dist = np.average(df['distance'])
    df_closest = df.iloc[
        (df['distance'] - average_dist).abs().argsort()[:1]]
    print("Average distance: {0}km. Closest pair: {1} - {2} {3}km".format(average_dist, df_closest['city1'].tolist()[0],
                                                                          df_closest['city2'].tolist()[0],
                                                                          df_closest['distance'].tolist()[0]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Description for my parser")
    parser.add_argument("-n", "--n", help="Example: Help argument", required=False, default="")
    argument = parser.parse_args()
    data = pd.read_csv("coordinates.csv", header=0)
    iterat = data.iterrows()
    result = pd.DataFrame(columns=["city1", "city2", "distance"])
    result_no_argument = pd.DataFrame(columns=["city1", "city2", "distance"])

    if argument.n != '':
        random_indices = random.sample(range(0,10), int(argument.n))
        for i in range(1, len(random_indices)):
            result.loc[i-1] = [data.iloc[i-1][0], data.iloc[i][0], great_circle(data.iloc[i-1][1], data.iloc[i-1][2], data.iloc[i][1], data.iloc[i][2])]
        sorted_df = result.sort_values('distance')
        print_result(sorted_df)
    else:
        lst = []
        for id1, id2 in zip(data.iterrows(), data.iloc[1:].iterrows()):
            lst.append([id1[1]['Name'], id2[1]['Name'],
                                     great_circle(id1[1]['Latitude'], id1[1]['Longitude'], id2[1]['Latitude'],
                                                  id2[1]['Longitude'])])
            df = pd.DataFrame(lst, columns=["city1", "city2", "distance"])
            result_no_argument = result_no_argument.append(df)
            sorted_result_no_argument = result_no_argument.sort_values('distance')
        sorted_result_no_argument = sorted_result_no_argument.drop_duplicates()
        print_result(sorted_result_no_argument)