from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from experiment_hillclimber import hillclimber
from experiment_simulated_annealing import simulated_annealing

from cable_connection_algorithm import cable_connection_algorithm as baseline
from cable_connection_algorithm_v1 import cable_connection_v1 as v1
from cable_connection_algorithm_v2 import cable_connection_v1 as v2
from cable_connection_algorithm_v3 import cable_connection_v1 as v3
from cable_connection_algorithm_v4 import cable_connection_v1 as v4
from cable_connection_algorithm_v5 import cable_connection_v1 as v5

import time
import json

def instance(cable_connection_algorithm, cable_connection_algorithm_name, max_time, district, T, slope):

    valid_state = 1
    
    while valid_state == 1:
    
        smartgrid = Smartgrid(district)
        
        battery, houses = smartgrid.get_data()
        
        invalid_state = random_state_generator(battery, houses)
        
        valid_state = make_solution(battery, invalid_state)
    
    valid_state, climb, iteration = simulated_annealing(max_time, valid_state, battery, T, slope, cable_connection_algorithm, smartgrid, cable_connection_algorithm_name)
    
    cables = smartgrid.cables
    
    return valid_state, iteration, min(climb), district, max_time, cable_connection_algorithm_name, cables, T, slope


def json_writer(valid_state, iteration, cost_shared, district, max_time, cable_connection_algorithm_name, cables, T, slope):
    
    # create empty data list
    data = []
    
    # first entry
    entry1 = {"district": district, "cost-shared": cost_shared, "iterations": iteration
    ,"time": max_time, "cable-connection-algorithm-name": cable_connection_algorithm_name, "T": T, "slope": slope}
    
    data.append(entry1)
    
    # loop to create remaining entries
    for battery, houses in valid_state.items():
    
        # create battery entry
        entry = {"location": f"{battery.x},{battery.y}", "capacity": battery.capacity,"houses": []}

        # loop for filling "houses" key of current battery entry
        for house in houses:

            string_path_cords = []
            
            # turn path cords into string
            for cords in cables[house.identification].path:
                string = f"{cords[0]},{cords[1]}"
                string_path_cords.append(string)
            
            # create house_entry
            house_entry = {"location": f"{house.x, house.y}", "output": house.capacity, "cables": string_path_cords}
            
            # append hous_entry to "houses" key 
            entry["houses"].append(house_entry)
            
        # append battery entry to data
        data.append(entry)     
    
    # create json file containing "data"
    with open(f'district{district}_{cable_connection_algorithm_name}_{cost_shared}$_{time}s.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)
        
    

def experiment(max_time):

    algos = [baseline, v1, v2, v3, v4, v5]
    
    names = ["b ", "v1", "v2", "v3", "v4", "v5"]
    
    district = "1"
    
    T = 40
    
    slope = 0.994
    
    cost_shared_list = []
    
    iterations_list = []
    
    for i in range(len(algos)):
    
        valid_state, iteration, cost_shared, district, max_time, cable_connection_algorithm_name, cables, T, slope = instance(algos[i], names[i], max_time, district, T, slope)
        
        json_writer(valid_state, iteration, cost_shared, district, max_time, cable_connection_algorithm_name, cables, T, slope)
        
        cost_shared_list.append(cost_shared)
        
        iterations_list.append(iteration)
        
        
    print("RESULTS")
    print("----------------------------------------------------------")
    
    for j in range(len(algos)):

        print(f"algo: {names[j]} | time: {max_time} | district: {district} | min cost: {cost_shared_list[j]} | iterations: {iterations_list[j]}")
        
if __name__ == "__main__":
    experiment(100)