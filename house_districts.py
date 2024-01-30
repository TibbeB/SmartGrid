import random
import math
from objects.battery import Battery
from main import Smartgrid
from itertools import permutations
from cable_connection_algorithm_v5 import cable_connection_v1
from quick_plotter import quick_plot


import random
import math
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    
def house_districts(batteries: dict, houses: dict) -> dict:
    """randomly distributes houses to batteries"""
    connections = {}
    district_capacity = 30


        # setting batteries as keys and empty lists as values
    for identification, battery in batteries.items():
        
        connections[battery] = []
    # Step 1: Determine the number of districts
    num_districts = 5
    
    kmeans = KMeans(num_districts)
    house_x = []
    house_y = []

    for house_id in houses:
        
        house_x.append(houses[house_id].x)
        house_y.append(houses[house_id].y)
        
    data = list(zip(house_x, house_y))
    
    kmeans = KMeans(num_districts)
    gefit = kmeans.fit(data)
    
    cluster_values = gefit.labels_.tolist()
    
    cluster_center = gefit.cluster_centers_.tolist()
    
    cluster_centers = {}
    
    
    
    for i, pair in enumerate(cluster_center):
        cluster_centers[i] = pair    
   
    asigned_batteries = []
    min_distance = float('inf')
    asigned_clusters = {}
    
    # connects batteries to clusters
    for cluster in cluster_centers:
    
        x_cluster = cluster_centers[cluster][0]
        y_cluster = cluster_centers[cluster][1]
        
        neares_battery = None
        
        for battery in batteries:
        
            if battery in asigned_batteries:
                continue
                
            x_battery = batteries[battery].x
            y_battery = batteries[battery].y
            
            distance = (abs(x_cluster - x_battery) ** 2 + abs(y_cluster - y_battery) ** 2) ** 0.5
            
            if distance < min_distance:
                distance = min_distance
                neares_battery = battery
                
        asigned_batteries.append(neares_battery)
        
        asigned_clusters[cluster] = neares_battery
        
    index = 0
    
    empty_clusters = [0, 1, 2, 3, 4]
    
    test = 0
    
    # asigning houses to batteries
    for clusters in cluster_values:
        
        battery_id = asigned_clusters[clusters]
        battery = batteries[battery_id]
        house = houses[index]     
        shortest_distance = float('inf')
        closest_cluster = 0

        x = cluster_center[clusters][0]
        y = cluster_center[clusters][1] 
        
        if (battery.occupied_capacity + house.capacity) < battery.capacity:
            test += 1
            battery.occupied_capacity += house.capacity
            connections[battery].append(house)
  
        else: 
            
            if clusters in empty_clusters:
                empty_clusters.remove(clusters)
                
            for cluster in empty_clusters:
        
                if cluster == clusters:
                    continue

                else:
                    x_test = cluster_center[cluster][0]
                    y_test = cluster_center[cluster][1]
                    
                    distance = (abs(x - x_test) ** 2 + abs(y - y_test) ** 2) ** 0.5
                    
                    if distance < shortest_distance:
                        shortest_distance = distance
                        closest_cluster = cluster 
                    
            battery_id = asigned_clusters[closest_cluster]
            battery = batteries[battery_id]
         
            battery.occupied_capacity += house.capacity
            connections[battery].append(house)
                    

            
        index += 1
        
            
    plt.scatter(house_x, house_y, c = kmeans.labels_)
    plt.show()
        
    print(len(connections[batteries[0]]) + len(connections[batteries[1]]) + len(connections[batteries[2]]) + len(connections[batteries[3]]) + len(connections[batteries[4]]))
    return connections

def house_districts_optimization(connections: dict) -> dict:

    # Generate permutations of values (lists)
    values_permutations = permutations(connections.values())
    
    lowest_cost = float('inf')
    best_dict = {}
    # Iterate through permutations
    for values_permutation in values_permutations:
        # Create a new dictionary for the current permutation
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
            
    cables = cable_connection_v1(best_dict, s.cables)
    quick_plot(best_dict, s.cables)
            
   

if __name__ == "__main__":
    # test code 
    s = Smartgrid("1")
    b, h = s.get_data()

    connections = house_districts(b, h)
    
    house_districts_optimization(connections)

    # for battery, houses in connections.items():
        # print("-----------------------------------------")
        # print(f"battery: {battery.identification}")
        # print(f"battery occupied capacity = {battery.occupied_capacity}")
        # c = 0
        # for house in houses:
            # c += 1
        # print(f"{c} houses")
    
    
    
