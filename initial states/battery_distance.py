import random
import math
from objects.battery import Battery
from main import Smartgrid

def battery_distance(batteries: dict, houses: dict) -> dict:
    """randomly distributes houses to batteries
    
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
        
        distances = {}
        distances[0] = (math.sqrt(abs(batteries[0].x - house.x)**2 + abs(batteries[0].y - house.y)**2))
        distances[1] = (math.sqrt(abs(batteries[1].x - house.x)**2 + abs(batteries[1].y - house.y)**2))
        distances[2] = (math.sqrt(abs(batteries[2].x - house.x)**2 + abs(batteries[2].y - house.y)**2))
        distances[3] = (math.sqrt(abs(batteries[3].x - house.x)**2 + abs(batteries[3].y - house.y)**2))
        distances[4] = (math.sqrt(abs(batteries[4].x - house.x)**2 + abs(batteries[4].y - house.y)**2))

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
        battery = batteries[min(distances, key=distances.get)]
        
        battery.occupied_capacity += house.capacity
        
        connections[battery].append(house)
            
            

         
    return connections

if __name__ == "__main__":
    # test code 
    s = Smartgrid("1")
    b, h = s.get_data()

    connections = battery_distance(b, h)
    print(connections)

    for battery, houses in connections.items():
        print("-----------------------------------------")
        print(f"battery: {battery.identification}")
        print(f"battery occupied capacity = {battery.occupied_capacity}")
        c = 0
        for house in houses:
            c += 1
        print(f"{c} houses")
