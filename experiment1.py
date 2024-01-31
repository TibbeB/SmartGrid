from main import Smartgrid
from algorithms.initial_state_algorithms.random_state_generator import random_state_generator
from algorithms.initial_state_algorithms.random_solution import make_solution
from algorithms.iterative_algorithms.experiment_hillclimber import hillclimber
from algorithms.iterative_algorithms.experiment_simulated_annealing import simulated_annealing
from algorithms.initial_state_algorithms.house_districts import house_districts, house_districts_optimization
from experiment import json_writer


from algorithms.cable_algoritmes.cable_connection_algorithm import cable_connection_algorithm as baseline
from algorithms.cable_algoritmes.cable_connection_algorithm_v1 import cable_connection_v1 as v1
from algorithms.cable_algoritmes.cable_connection_algorithm_v2 import cable_connection_v1 as v2
from algorithms.cable_algoritmes.cable_connection_algorithm_v3 import cable_connection_v1 as v3
from algorithms.cable_algoritmes.cable_connection_algorithm_v4 import cable_connection_v1 as v4
from algorithms.cable_algoritmes.cable_connection_algorithm_v5 import cable_connection_v1 as v5

import time
import json
import typing
from typing import Callable, Dict, List, Tuple, Any

def instance(smartgrid: Smartgrid, valid_state: dict[object, list[object]], battery: list[object], cable_connection_algorithm: Callable[dict[object, list[object]],
    dict[int, object]], cable_connection_algorithm_name: str, max_time: int,
    district: str, T: int, slope: int) -> tuple[dict[object, list[object]], int, int, int, dict[int, object]]:
    """
    Runs simulated annealing hillclimber for a certain time using a given cable connection algorithm.
    
    pre:
    - smartgrid (object): smartgrid instance
    - valid_state (dict[object, list[object]]): the state
    - battery (object): batteries list
    - cable_connection_algorithm (Callable): cable connection algorithm.
    - cable_connection_algorithm_name (str): name of the cable connection algorithm.
    - max_time (int): runtime of hillclimber
    - district (str): The district ("1", "2", or "3")
    - T (int): temperature for simulated annealing
    - slope (int): slope for simulated annealing
    post:
    - returns valid_state (int): state after optimization
    - returns iteration (int): number of iterations
    - returns min_climb (int): minimum climb value obtained
    - returns cables (Dict[int, object]): resulting cables configuration
    """
    
    # call simulated annealing
    valid_state, climb, iteration = simulated_annealing(max_time, valid_state, battery,
    T, slope, cable_connection_algorithm, smartgrid, cable_connection_algorithm_name)
    
    cables = smartgrid.cables
    
    return valid_state, iteration, min(climb), cables

def experiment(district: str, max_time: int, T: int, slope: int) -> None:
    """
    perform experiment by calling functions 'instance' and 'json_writer' with different cable connection algorithms
    
    pre:
    - district (str): The district ("1", "2", or "3")
    - max_time (int): runtime of hillclimber
    post:
    - returns N json_files
    - prints results in terminal
    """

    algos = [baseline, v1, v2, v3, v4, v5]
    
    names = ["b ", "v1", "v2", "v3", "v4", "v5"]
    
    cost_shared_list = []
    
    iterations_list = []
    
    valid_state = 1
    
    while valid_state == 1:
        
        # create smartgrid instance
        smartgrid = Smartgrid(district)
        
        battery, houses = smartgrid.get_data()
        
        # create house districts
        valid_state = house_districts(battery, houses)
        
        # optimalize house districts
        valid_state = house_districts_optimization(smartgrid, valid_state)
    
    for i in range(len(algos)):
    
        valid_state, iteration, cost_shared, cables = instance(smartgrid, valid_state, battery, algos[i], names[i], max_time, district, T, slope)
        
        entry1 = [iteration, cost_shared, district, max_time, names[i], T, slope]
        
        entry1_names = ["iterations","cost-shared", "district", "time", "cable-connection-algorithm-name", "T", "slope"]
        
        json_writer(valid_state, entry1, entry1_names, cables)
        
        cost_shared_list.append(cost_shared)
        
        iterations_list.append(iteration)
        
        
    print("RESULTS")
    print("----------------------------------------------------------")
    
    for j in range(len(algos)):

        print(f"algo: {names[j]} | time: {max_time} | district: {district} | min cost: {cost_shared_list[j]} | iterations: {iterations_list[j]}")
        
if __name__ == "__main__":
    experiment("1", 1, 40, 0.994)