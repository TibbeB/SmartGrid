from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from quick_plotter import quick_plot

import matplotlib.pyplot as plt
from numpy import random
import copy
import time

def random_switch(batteries, connections):
    state_copy = copy.deepcopy(connections)  # Create a deep copy of the state
    
    # Create a mapping between original batteries and their copies
    keys_connections = []
    for key in connections:
        keys_connections.append(key)

    keys_copy = []
    for key in state_copy:
        keys_copy.append(key)

    battery_mapping = {}
    for i in range(len(keys_connections)):
        battery_mapping[keys_connections[i]] = keys_copy[i]

    while True:
        battery_1, battery_2 = 0, 0
        while battery_1 == battery_2:
            battery_1 = batteries[random.choice([0, 1, 2, 3, 4])]
            battery_2 = batteries[random.choice([0, 1, 2, 3, 4])]

        index_1 = random.randint(len(state_copy[battery_mapping[battery_1]]))
        index_2 = random.randint(len(state_copy[battery_mapping[battery_2]]))

        cap_1 = state_copy[battery_mapping[battery_1]][index_1].capacity
        cap_2 = state_copy[battery_mapping[battery_2]][index_2].capacity

        diff = abs(cap_1 - cap_2)

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

    if cap_1 > cap_2:
        battery_1.occupied_capacity += diff
        battery_2.occupied_capacity -= diff
    else:
        battery_1.occupied_capacity -= diff
        battery_2.occupied_capacity += diff

    return state_copy


def hillclimber(smartgrid, valid_state, battery, cable_connection_algorithm, cable_connection_algorithm_name, max_time):    

    climb = []
    iteration = []
 
    cable_connection_algorithm(valid_state, smartgrid.cables)
    cost = smartgrid.cost_shared(valid_state)
    climb.append(cost)
    iteration.append(0)

    succes = 0
    
    start = time.time()
    j = 1
    
    while time.time() - start < max_time:
                
        climb.append(cost)
        iteration.append(j + 1)
        
        for key, cable in smartgrid.cables.items():
            cable.clear_cable()

        new_state = random_switch(battery, valid_state)
        cable_connection_algorithm(new_state, smartgrid.cables)
        new_cost = smartgrid.cost_shared(new_state)

        if new_cost < cost:
            succes += 1
            valid_state = new_state
            cost = new_cost
            
            new_batteries = []
            for key in valid_state:
                new_batteries.append(key)

            for i in range(5):
                battery[i] = new_batteries[i]
        
        print(f"hillclimber | cable connection algo: {cable_connection_algorithm_name} | run: {j} | successes: {succes}")
        j += 1
    return valid_state, climb, j, succes

if __name__ == '__main__':
    # make state
    state = 1
    while state == 1:
        s = Smartgrid("1")
        b, h = s.get_data()
        random_state = random_state_generator(b, h)
        state = make_solution(b, random_state)
    
    # hillclimb
    for i in range(1):
        N = 100
        b_or = b.copy()
        peak_state, cost_climb, iteration, succes = hillclimber(s, N, state, b_or)
        print(min(cost_climb))
        print(succes)

    plt.plot(iteration, cost_climb)
    plt.savefig("hillclimb.png")
    plt.show()

    

