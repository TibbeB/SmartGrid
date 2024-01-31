from numpy import random
import copy
import time

def random_switch(b, state):
    """Randomly switches two houses from different batteries,
    without going over the batteries capacity.

    Pre:
        b (dict[int: object]): list of the battery objects
        state (dict[object: list[object]]): The distribution of houses over the batteries

    Post:
        state_copy (dict[object: list[object]]): New state
    """    

    # Create a deep copy of the state
    state_copy = copy.deepcopy(state)
    
    # Create a mapping between original batteries and their copies
    keys_connections = []
    for key in state:
        keys_connections.append(key)

    keys_copy = []
    for key in state_copy:
        keys_copy.append(key)

    battery_mapping = {}
    for i in range(len(keys_connections)):
        battery_mapping[keys_connections[i]] = keys_copy[i]

    # Find two houses that can be switched 
    # without going over the batteries capacities
    while True:

        # Get two random batteries
        battery_1, battery_2 = 0, 0
        while battery_1 == battery_2:
            battery_1 = b[random.choice([0, 1, 2, 3, 4])]
            battery_2 = b[random.choice([0, 1, 2, 3, 4])]

        index_1 = random.randint(len(state_copy[battery_mapping[battery_1]]))
        index_2 = random.randint(len(state_copy[battery_mapping[battery_2]]))

        # Get two random houses
        cap_1 = state_copy[battery_mapping[battery_1]][index_1].capacity
        cap_2 = state_copy[battery_mapping[battery_2]][index_2].capacity

        diff = abs(cap_1 - cap_2)

        # Check if the capacity isn't exceeded
        if cap_1 > cap_2:
            if battery_1.occupied_capacity + diff < 1506:
                break
        else:
            if battery_2.occupied_capacity + diff < 1506:
                break

    # Switch the houses
    house1 = state_copy[battery_mapping[battery_1]][index_1]
    state_copy[battery_mapping[battery_1]][index_1] = state_copy[battery_mapping[battery_2]][index_2]
    state_copy[battery_mapping[battery_2]][index_2] = house1

    # Update the occupied capacities of the batteries
    if cap_1 > cap_2:
        battery_1.occupied_capacity += diff
        battery_2.occupied_capacity -= diff
    else:
        battery_1.occupied_capacity -= diff
        battery_2.occupied_capacity += diff

    return state_copy


def hillclimber(smartgrid, valid_state, battery, cable_connection_algorithm, 
    cable_connection_algorithm_name, max_time):    
    """A hillclimber that makes small changes to the state and saves the best one.

    Pre:
        smartgrid (Smartgrid): Smartgrid class
        valid_state (dict[object: list[object]]): The distribution of houses over the batteries
        battery (dict[int: object]): list of the battery objects
        cable_connection_algorithm (Callable[dict[object, list[object]]): cable connetcion algorithm
        cable_connection_algorithm_name (str): cable conection algorithm name
        max_time (int): for how long the hillclimber is runs

    Post:
        state (dict[object: list[object]]): The distribution of houses over the batteries
        climb (list[int]): list of the costs of all the states generated in the hillclimber
        j (int): iterations
        succes (int): number of switches that resulted in a better state (lower cost)
    """ 
    # make lists to store data
    climb = []
    iteration = []
    
    # Set start point of the climb
    cable_connection_algorithm(valid_state, smartgrid.cables)
    cost = smartgrid.cost_shared(valid_state)
    climb.append(cost)
    iteration.append(0)

    succes = 0
    
    start = time.time()
    j = 1
    
    # Make small changes
    while time.time() - start < max_time:
        
        # Add new cost to data
        climb.append(cost)
        iteration.append(j + 1)
        
        # Clear recently layed cables
        for key, cable in smartgrid.cables.items():
            cable.clear_cable()
        
        # Make new state and calculate the cost of the new state
        new_state = random_switch(battery, valid_state)
        cable_connection_algorithm(new_state, smartgrid.cables)
        new_cost = smartgrid.cost_shared(new_state)
        
        # check if new state is better (lower cost)
        # and save the state if this is the case
        if new_cost < cost:
            succes += 1
            valid_state = new_state
            cost = new_cost
            
            new_batteries = []
            for key in valid_state:
                new_batteries.append(key)

            for i in range(5):
                battery[i] = new_batteries[i]
                
        if j % 100 == 0:
            print(f"hillclimber | cable connection algo: {cable_connection_algorithm_name} | run: {j} | successes: {succes}")
        j += 1
    return valid_state, climb, j, succes



    

