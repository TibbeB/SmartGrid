import math
from objects.battery import Battery
from itertools import permutations
from cable_connection_algorithm_v5 import cable_connection_v1
from sklearn.cluster import KMeans
from typing import Dict, List

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    

def house_districts(batteries: dict[int, object], houses: dict[int, object]) -> dict[object, list[object]]:
    """
    Puts houses into districts and announces districts to batteries.

    Args:
        batteries (Dict[int, Battery]): A dictionary where keys are battery identifications and values are Battery objects.
        houses (Dict[int, House]): A dictionary where keys are house identifications and values are House objects.

    Returns:
        connections (Dict[Battery, List[House]]): A dictionary mapping batteries to the list of houses connected to them.
    """
    # initialize connections dictionary
    connections: dict[object, list[object]] = {}  

    # setting batteries as keys and empty lists as values
    for identification, battery in batteries.items():
        connections[battery] = []

    num_districts = 5
    
    # using KMeans clustering to determine districts
    kmeans = KMeans(num_districts)
    house_x = []
    house_y = []

    # extracting house coordinates for clustering
    for house_id, house in houses.items():
        house_x.append(house.x)
        house_y.append(house.y)
        
    data = list(zip(house_x, house_y))
    
    # fitting KMeans to data
    gefit = kmeans.fit(data)
    
    cluster_values = gefit.labels_.tolist()
    cluster_center = gefit.cluster_centers_.tolist()
    
    # storing cluster centers in a dictionary
    cluster_centers: dict[int, tuple[float, float]] = {}
    for i, pair in enumerate(cluster_center):   
        cluster_centers[i] = pair    
   
    asigned_batteries: list[int] = [] 
    min_distance = float('inf')  
    asigned_clusters: dict[int, int] = {}  
    
    # connects batteries to clusters
    for cluster, center in cluster_centers.items():
        x_cluster, y_cluster = center
        
        neares_battery = None
        
        for battery_id, battery in batteries.items():
            if battery_id in asigned_batteries:
                continue
                
            x_battery = battery.x
            y_battery = battery.y
            
            # calculating distance between battery and cluster center
            distance = (abs(x_cluster - x_battery) ** 2 + abs(y_cluster - y_battery) ** 2) ** 0.5
            
            if distance < min_distance:
                distance = min_distance
                neares_battery = battery_id
                
        asigned_batteries.append(neares_battery)
        asigned_clusters[cluster] = neares_battery
        
    index = 0
    empty_clusters = [0, 1, 2, 3, 4]
    test = 0
    
    # assigning houses to batteries
    for clusters in cluster_values:
        battery_id = asigned_clusters[clusters]
        battery = batteries[battery_id]
        house = houses[index]     
        shortest_distance = float('inf')
        closest_cluster = 0

        x, y = cluster_center[clusters]
        
        # if the battery has capacity for the house, assign it
        if (battery.occupied_capacity + house.capacity) < battery.capacity:
            test += 1
            battery.occupied_capacity += house.capacity
            connections[battery].append(house)
        else: 
            # if battery is full, assign the house to the closest empty cluster
            if clusters in empty_clusters:
                empty_clusters.remove(clusters)
                
            for cluster in empty_clusters:
                if cluster == clusters:
                    continue
                else:
                    x_test, y_test = cluster_center[cluster]
                    distance = (abs(x - x_test) ** 2 + abs(y - y_test) ** 2) ** 0.5
                    
                    if distance < shortest_distance:
                        shortest_distance = distance
                        closest_cluster = cluster 
                    
            battery_id = asigned_clusters[closest_cluster]
            battery = batteries[battery_id]
            battery.occupied_capacity += house.capacity
            connections[battery].append(house)
            
        index += 1
        
    return connections
            

def house_districts_optimization(s, connections: dict) ->  dict[object, list[object]]:

    # generate permutations of values (lists)
    values_permutations = permutations(connections.values())
    
    lowest_cost = float('inf')
    best_dict = {}
    
    # iterate through permutations
    for values_permutation in values_permutations:
        # create a new dictionary for the current permutation
        new_dict = {}
        for key, value in zip(connections.keys(), values_permutation):
            new_dict[key] = value
        
        
        cable_connection_v1(new_dict, s.cables)
        new_cost = s.cost_shared(new_dict)
        
        if new_cost < lowest_cost:
            lowest_cost = new_cost
            best_dict = new_dict
            
        # clear cables
        for key, cable in s.cables.items():
            cable.clear_cable()

    return best_dict
            

        
    
    
