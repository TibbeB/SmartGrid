from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from experiment_hillclimber import hillclimber
from house_districts import house_districts, house_districts_optimization
import typing
from typing import Callable, Dict, List, Tuple, Any

from cable_connection_algorithm import cable_connection_algorithm as baseline
from cable_connection_algorithm_v1 import cable_connection_v1 as v1
from cable_connection_algorithm_v2 import cable_connection_v1 as v2
from cable_connection_algorithm_v3 import cable_connection_v1 as v3
from cable_connection_algorithm_v4 import cable_connection_v1 as v4
from cable_connection_algorithm_v5 import cable_connection_v1 as v5

import time
import json


def instance(smartgrid: Smartgrid, valid_state: dict[object, list[object]], battery: list[object], cable_connection_algorithm: Callable[dict[object, list[object]],
    dict[int, object]], cable_connection_algorithm_name: str, max_time: int,
    district: str) -> tuple[dict[object, list[object]], int, int, int, dict[int, object]]:
    """
    Runs hillclimber for a certain time using a given cable connection algorithm.
    
    pre:
    - smartgrid (object): smartgrid instance
    - valid_state (dict[object, list[object]]): the state
    - battery (object): batteries list
    - cable_connection_algorithm (Callable): cable connection algorithm.
    - cable_connection_algorithm_name (str): name of the cable connection algorithm.
    - max_time (int): runtime of hillclimber
    - district (str): The district ("1", "2", or "3")
    post:
    - returns valid_state (int): state after optimization
    - returns iteration (int): number of iterations
    - returns success (int): ammount of succesfull adjustments
    - returns min_climb (int): minimum climb value obtained
    - returns cables (Dict[int, object]): resulting cables configuration
    """
    
    # call hillclimber
    valid_state, climb, iteration, succes = hillclimber(smartgrid, valid_state, battery,
    cable_connection_algorithm, cable_connection_algorithm_name, max_time)
    
    cables = smartgrid.cables
    
    return valid_state, iteration, succes, min(climb), cables


def json_writer(valid_state: dict[object, list[object]],list_entry1: list[Any], list_entry1_names: list[str],
    cables: dict[int, object]) -> None:
    """
    writes an json file that represents input state
    
    pre:
    - valid_state (Dict[object, List[object]]): dictionary representing the state
    - list_entry1 (list[Any]): contains values that you want to save in entry1
    - list_entry1_names list[str]: contains names of values that you want to save in entry1
    - cables (Dict[int, object]): dictionary representing the cables configuration
    post:
    - returns a json file representing the input state is created
    """
    
    # create empty data list
    data = []
    
    # first entry
    entry1 = {}
    for i, item in enumerate(list_entry1):
        entry1[list_entry1_names[i]] = item
    
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
    
    string = ""
    
    # write json file containing "data"
    for j in range(len(list_entry1_names)):
    
        string += f"{list_entry1_names[j][0]}{list_entry1[j]}"
        
    string += ".json"
    
    with open(string, 'w') as json_file:
    
        json.dump(data, json_file, indent=2)
        
    
def experiment(district: str, max_time: int) -> None:
    """
    perform experiment by calling functions 'instance' and 'json_writer' with different cable connection algorithms
    
    pre:
    - district (str): The district ("1", "2", or "3")
    - max_time (int): runtime of hillclimber
    post:
    - returns N json_files
    - prints results in terminal
    """
    
    # list cable connections algorithms
    algos = [baseline, v1, v2, v3, v4, v5]
    
    # list of their respective names
    names = ["b ", "v1", "v2", "v3", "v4", "v5"]
    
    cost_shared_list = []
    
    iterations_list = []
    
    succes_list = []
    
    valid_state = 1
    
    while valid_state == 1:
        
        # create smartgrid instance
        smartgrid = Smartgrid(district)
        
        battery, houses = smartgrid.get_data()
        
        # create house districts
        valid_state = house_districts(battery, houses)
        
        # optimalize house districts
        valid_state = house_districts_optimization(smartgrid, valid_state)
    
    # loop trough algorithms
    for i in range(len(algos)):
        
        # call instance
        valid_state, iteration, succes, cost_shared, cables = instance(smartgrid, valid_state, battery, algos[i], names[i], max_time, district)
        
        entry1 = [iteration, succes, cost_shared, district, max_time, names[i]]
        
        entry1_names = ["iterations", "succes", "cost-shared", "district", "time", "cable-connection-algorithm-name"]
        
        # write json file
        json_writer(valid_state, entry1, entry1_names, cables)
        
        cost_shared_list.append(cost_shared)
        
        iterations_list.append(iteration)
        
        succes_list.append(succes)
    
    # print results in terimnal
    print("RESULTS")
    print("----------------------------------------------------------")
    
    for j in range(len(algos)):

        print(f"algo: {names[j]} | time: {max_time} | district: {district} | min cost: {cost_shared_list[j]} | iterations: {iterations_list[j]} | successes: {succes_list[j]} | s/i: {succes_list[j]/iterations_list[j]}")

     
if __name__ == "__main__":
    experiment("1", 1)