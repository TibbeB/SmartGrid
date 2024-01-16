import random
from main import Smartgrid

def house_distribution(batteries: dict, houses: dict) -> dict:
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
        
        # pick random battery
        battery = random.choice(list(batteries.values()))
        
        # pick random house and remove house from houses list
        house = houses.pop(random.choice(list(houses.values())).identification)
        
        # append house capacity to battery occupied capacity
        battery.occupied_capacity += house.capacity
        
        # append house to battery
        connections[battery].append(house)
         
    return connections

if __name__ == "__main__":  
    s = Smartgrid("1")
    b, h = s.get_data()

    connections = house_distribution(b, h)

    for battery, houses in connections.items():
        print("-----------------------------------------")
        print(f"battery: {battery.identification}")
        print(f"battery occupied capacity = {battery.occupied_capacity}")
        c = 0
        for house in houses:
            c += 1
        print(f"{c} houses")
