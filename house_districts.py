import random
import math
from objects.battery import Battery
from main import Smartgrid

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
    
    for clusters in cluster_values:
        
        battery_id = asigned_clusters[clusters]
        battery = batteries[battery_id]
        house = houses[index]
        
        shortest_distance = float('inf')
        closest_cluster = 0

        x = cluster_center[clusters][0]
        y = cluster_center[clusters][1]

        battery.occupied_capacity += house.capacity
        connections[battery].append(house)
       
        index += 1
        
        
        
        
    # for battery in connections:
        # if 
        # for house in connections[battery]
            
        
    plt.scatter(house_x, house_y, c = kmeans.labels_)
    plt.show()
        
    
    return connections



if __name__ == "__main__":
    # test code 
    s = Smartgrid("1")
    b, h = s.get_data()

    connections = house_districts(b, h)

    # for battery, houses in connections.items():
        # print("-----------------------------------------")
        # print(f"battery: {battery.identification}")
        # print(f"battery occupied capacity = {battery.occupied_capacity}")
        # c = 0
        # for house in houses:
            # c += 1
        # print(f"{c} houses")
    
    
    print(s.cost_shared(connections))    
    
