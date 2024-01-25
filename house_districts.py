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
    
    clusters = {}
    
    for i, pair in enumerate(cluster_center):
        clusters[i] = pair    
        
    
    for cluster in clusters:
        
        x = clusters[cluster][0]
        y = clusters[cluster][1]
        
        
        
    print(cluster_values.count(0))
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
    
