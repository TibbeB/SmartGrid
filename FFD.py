import numpy as np

def even_distribution(batteries: dict, houses: dict) -> {object:[object]}:
    """ evenly distributes the max outputs of the houses over the batteries
    
    pre: 
    - batteries must be a dict, houses must be a dict
    - csv_reader is called

    post:
    - returns a dict or 1 if a max capacity is exceeded"""

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

    for i in range(len(batteries)):
        batteries[i].occupied_capacity = battery_sums[i]

    return connections

def x_y_path(self, dict_connections):

    # iterates trough all batteries in the dictionaries
    for battery in dict_connections:
        x_battery = battery.x
        y_battery = battery.y
        
        connections = dict_connections[battery]

        # iterates trough all houses at a specific battery
        for houses in connections:
            cable = self.cables[houses.identification]

            x_house = houses.x
            y_house = houses.y
            
            x_distance = x_battery - x_house
            y_distance = y_battery - y_house
            
            # iterates trough all steps from the house to the battery
            # determines left or right
            for x_steps in range(abs(x_distance)):
                if x_distance < 0:
                    cable.left()
                    
                else:
                    cable.right()
            
            # iterates trough all steps from the house to the battery
            # determines up or down
            for y_steps in range(abs(y_distance)):
                if y_distance < 0:
                    cable.down()
                    
                else:
                    cable.up()