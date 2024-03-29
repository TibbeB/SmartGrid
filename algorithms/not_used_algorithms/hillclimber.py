from main import Smartgrid
from numpy import random
import copy


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


def hillclimber(s, N, state, b, algo):
    """A hillclimber that makes small changes to the state and saves the best one.

    Pre:
        s (Smartgrid): Smartgrid class
        N (int): Number of times the hillclimber switches two houses
        state (dict[object: List[object]]): The distribution of houses over the batteries
        b (dict[int: object]): List of the battery objects

    Post:
        state (dict[object: list[object]]): The distribution of houses over the batteries
        climb (list[int]): List of the costs of all the states generated in the hillclimber
        iteration (list[int]): List of corresponding iteration to to costs in climb
        succes (int): Number of switches that resulted in a better state (lower cost)
    """        
    # make lists to store data
    climb = []
    iteration = []
 
    # Set start point of the climb
    algo(state, s.cables)
    cost = s.cost_shared(state)
    climb.append(cost)
    iteration.append(0)

    # Make small changes
    succes = 0
    
    j = 0
    
    for i in range(N):

        # Prints every 1000 interations that the hillclimber is still going
        if i % 1000 == 0:
            print(i)

        # Add new cost to data
        climb.append(cost)
        iteration.append(i + 1)

        # Clear recently layed cables
        for key, cable in s.cables.items():
            cable.clear_cable()

        # Make new state and calculate the cost of the new state
        new_state = random_switch(b, state)
        algo(new_state, s.cables)
        new_cost = s.cost_shared(new_state)

        # check if new state is better (lower cost)
        # and save the state if this is the case
        if new_cost < cost:
            succes += 1
            state = new_state
            cost = new_cost
            
            new_batteries = []
            for key in state:
                new_batteries.append(key)

            for i in range(5):
                b[i] = new_batteries[i]
        j += 1

    return state, climb, j, succes



    

