import numpy as np

def even_distribution(batteries, houses):
    """ Evenly distributes the max outputs of the houses over the batteries
    
    pre: batteries must be a dict, houses must be a dict

    post: returns a dict or 1 if a max capacity is exceeded"""

    connections = {}

    # making list of houses sorted from large to small max outputs
    house_objects = []
    for key, value in houses.items():
        house_objects.append(value)

    house_objects.sort(key=lambda x: x.capacity)
    reverse = house_objects[::-1]
    
    # setting keys in connection to batteries
    for i in range(len(batteries)):
        connections[batteries[i]] = []

    # Destributing the houses max outputs evenly over the batteries
    # using the "First Fit Decreasing" algorithm 
    battery_sums = [0 for i in range(len(batteries))]
    for j in reverse:
        output_house = j.capacity
        battery_sums[np.argmin(battery_sums)] += output_house
        connections[batteries[np.argmin(battery_sums)]].append(j)

    if battery_sums[np.argmax(battery_sums)] > 1506:
        return 1

    return connections

    





