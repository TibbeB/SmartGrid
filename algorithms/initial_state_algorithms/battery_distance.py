import random
import math

from algorithms.initial_state_algorithms.objects.battery import Battery


def battery_distance(batteries: dict[int, object], houses: dict[int, object]) -> dict[object, list[object]]:
    """distributes houses to batteries based on distance.
    
    pre:
    - batteries is a dict
    - houses is a dict
    
    post:
    - connection is a dict filled with battery objects as keys
    - its values are lists of houses objects"""

    connections = {}
    
    
    # setting batteries as keys and empty lists as values
    for identification, battery in batteries.items():
        connections[battery] = []

    while len(houses) > 0:
    
        house = houses.pop(random.choice(list(houses.values())).identification)
        
        # calculating distances from each house to every battery
        distances = {}
        distances[0] = (math.sqrt(abs(batteries[0].x - house.x)**2 + abs(batteries[0].y - house.y)**2))
        distances[1] = (math.sqrt(abs(batteries[1].x - house.x)**2 + abs(batteries[1].y - house.y)**2))
        distances[2] = (math.sqrt(abs(batteries[2].x - house.x)**2 + abs(batteries[2].y - house.y)**2))
        distances[3] = (math.sqrt(abs(batteries[3].x - house.x)**2 + abs(batteries[3].y - house.y)**2))
        distances[4] = (math.sqrt(abs(batteries[4].x - house.x)**2 + abs(batteries[4].y - house.y)**2))

        # testing if a battery is full
        if batteries[0].occupied_capacity > batteries[0].capacity:
           distances.pop(0)
        
        if batteries[1].occupied_capacity > batteries[1].capacity:
            distances.pop(1)
            
        if batteries[2].occupied_capacity > batteries[2].capacity:
            distances.pop(2)
            
        if batteries[3].occupied_capacity > batteries[3].capacity:
            distances.pop(3)
       
        if batteries[4].occupied_capacity > batteries[4].capacity:
            distances.pop(4)
            
        # looking for closest battery that is not full
        battery = batteries[min(distances, key=distances.get)]        
        battery.occupied_capacity += house.capacity
        connections[battery].append(house)

    return connections

    
