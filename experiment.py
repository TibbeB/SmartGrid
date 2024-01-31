
from main import Smartgrid
from algorithms.initial_state_algorithms.random_state_generator import random_state_generator
from algorithms.initial_state_algorithms.random_solution import make_solution
from algorithms.iterative_algorithms.experiment_hillclimber import hillclimber as experiment_hillclimber
from algorithms.initial_state_algorithms.house_districts import house_districts, house_districts_optimization
from algorithms.not_used_algorithms.hillclimber import hillclimber
import typing
from typing import Callable, Dict, List, Tuple, Any

from algorithms.initial_state_algorithms.random_state_generator import random_state_generator
from algorithms.initial_state_algorithms.random_solution import make_solution
from algorithms.initial_state_algorithms.battery_distance import battery_distance

from algorithms.cable_algoritmes.cable_connection_algorithm import cable_connection_algorithm as baseline
from algorithms.cable_algoritmes.cable_connection_algorithm_v1 import cable_connection_v1 as v1
from algorithms.cable_algoritmes.cable_connection_algorithm_v2 import cable_connection_v1 as v2
from algorithms.cable_algoritmes.cable_connection_algorithm_v3 import cable_connection_v1 as v3
from algorithms.cable_algoritmes.cable_connection_algorithm_v4 import cable_connection_v1 as v4
from algorithms.cable_algoritmes.cable_connection_algorithm_v5 import cable_connection_v1 as v5
from algorithms.cable_algoritmes.dijkstra import dijkstra as d
from algorithms.cable_algoritmes.single_line_cable_connection_algorithm import single_line_cable_connection_algorithm as s

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
    valid_state, climb, iteration, succes = experiment_hillclimber(smartgrid, valid_state, battery,
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
        
    
def experiment(district: str, max_time: int, N: int) -> None:
    """
    perform experiment by calling functions 'instance' and 'json_writer' with different cable connection algorithms
    
    pre:
    - district (str): The district ("1", "2", or "3")
    - max_time (int): runtime of hillclimber
    - N (int): how many unque states generated
    post:
    - returns N json_files
    - prints results in terminal
    """
    init_n = [1,2,3]
    
    for item in init_n:
    
        # list cable connections algorithms
        algos = [baseline, v1, v2, v3, v4, v5, d, s]
        
        # list of their respective names
        names = ["b ", "v1", "v2", "v3", "v4", "v5", "d", "s"]
        
        valid_states = [[],[],[],[],[],[],[],[]]
        
        cost_shared_list = [[],[],[],[],[],[],[],[]]
            
        iterations_list = [[],[],[],[],[],[],[],[]]
        
        succes_list = [[],[],[],[],[],[],[],[]]
        
        cables_states = [[],[],[],[],[],[],[],[]]
        
        for k in range(N):
            
            valid_state = 1
            
            while valid_state == 1:
                
                # create smartgrid instance
                smartgrid = Smartgrid(district)
                
                battery, houses = smartgrid.get_data()
                
                if item == 1:
                    # create house districts
                    valid_state = house_districts(battery, houses)
                    
                if item == 2:
                    valid_state = random_state_generator(battery, houses)
                    valid_state = make_solution(battery, valid_state)
                    
                if item == 3:
                    valid_state = battery_distance(battery, houses)
                    valid_state = make_solution(battery, valid_state)
                    
                
            # loop trough algorithms
            for i in range(len(algos)):
                
                if item == 1:
                    # optimalize house districts
                    valid_state = house_districts_optimization(algos[i], smartgrid, valid_state)
                    
                # call instance
                valid_state, iteration, succes, cost_shared, cables = instance(smartgrid, valid_state, battery, algos[i], names[i], max_time, district)
                
                valid_states[i].append(valid_state)
                
                cost_shared_list[i].append(cost_shared)
                
                iterations_list[i].append(iteration)
                
                succes_list[i].append(succes)
                
                cables_states[i].append(cables)
        
        index_list = []
        
        for sum_costs in cost_shared_list:
            index_list.append(sum_costs.index(min(sum_costs)))
            
        for index, index_min_cost in enumerate(index_list):
            json_writer(valid_states[index][index_min_cost], [iterations_list[index][index_min_cost], succes_list[index][index_min_cost], cost_shared_list[index][index_min_cost],district, max_time, names[index]], ["iterations", "succes", "cost-shared", "district", "time", "cable-connection-algorithm-name"], cables_states[index][index_min_cost])
            
        # print avg results in terminal
        print(f"AVERAGE RESULTS | hillclimber: {item}")
        print("----------------------------------------------------------")
        
        for j in range(len(algos)):

            print(f"algo: {names[j]} | time: {max_time} | district: {district} | avg cost: {sum(cost_shared_list[j])/len(cost_shared_list[j])} | avg iterations: {sum(iterations_list[j])/len(iterations_list[j])} | avg successes: {sum(succes_list[j])/len(succes_list[j])}")

        # print avg results in terimnal
        print(f"MINIMUM RESULTS | hillclimber: {item}")
        print("----------------------------------------------------------")
        
        for x in range(len(algos)):

            print(f"algo: {names[x]} | time: {max_time} | district: {district} | avg cost: {cost_shared_list[x][index_list[x]]} | avg iterations: {iterations_list[x][index_list[x]]} | avg successes: {succes_list[x][index_list[x]]}")
    
    
def experiment_iterations(district: str, n: int, N: int):
    """
    perform experiment by calling functions 'instance' and 'json_writer' with different cable connection algorithms

    pre:
    - district (str): The district ("1", "2", or "3")
    - n (int): how many unque states generated
    - N (int): how many itterations in hillclimber
    post:
    - returns N json_files
    - prints results in terminal
    """
    
    initial_state_algos = [1,2,3]
    
    for item in initial_state_algos:
    
        # list cable connections algorithms
        algos = [baseline, v1, v2, v3, v4, v5, d, s]

        # list of their respective names
        names = ["b ", "v1", "v2", "v3", "v4", "v5", "d", "s"]

        valid_states = [[],[],[],[],[],[],[],[]]

        cost_shared_list = [[],[],[],[],[],[],[],[]]
            
        iterations_list = [[],[],[],[],[],[],[],[]]

        succes_list = [[],[],[],[],[],[],[],[]]

        cables_states = [[],[],[],[],[],[],[],[]]

        for k in range(n):
            
            valid_state = 1
            
            while valid_state == 1:
                
                # create smartgrid instance
                smartgrid = Smartgrid(district)
                
                battery, houses = smartgrid.get_data()
                
                # create house districts
                valid_state = house_districts(battery, houses)
                
                if item == 1:
                    # create house districts
                    valid_state = house_districts(battery, houses)
                    
                if item == 2:
                    valid_state = random_state_generator(battery, houses)
                    valid_state = make_solution(battery,valid_state)
                    
                if item == 3:
                    valid_state = battery_distance(battery, houses)
                    valid_state = make_solution(battery,valid_state)
            
            # loop trough algorithms
            for i in range(len(algos)):
            
                if item == 1:
                    # optimalize house districts
                    valid_state = house_districts_optimization(algos[i], smartgrid, valid_state)
            
                # optimalize house districts
                valid_state = house_districts_optimization(algos[i], smartgrid, valid_state)
                
                # call hillclimber
                valid_state, climb, iteration, succes = hillclimber(smartgrid, N, valid_state, battery, algos[i])
                
                cables = smartgrid.cables
                
                valid_states[i].append(valid_state)
                
                cost_shared_list[i].append(min(climb))
                
                iterations_list[i].append(iteration)
                
                succes_list[i].append(succes)
                
                cables_states[i].append(cables)

        index_list = []

        for sum_costs in cost_shared_list:
            index_list.append(sum_costs.index(min(sum_costs)))
            
        for index, index_min_cost in enumerate(index_list):
            json_writer(valid_states[index][index_min_cost], [iterations_list[index][index_min_cost], succes_list[index][index_min_cost], cost_shared_list[index][index_min_cost],district, names[index]], ["iterations", "succes", "cost-shared", "district", "cable-connection-algorithm-name"], cables_states[index][index_min_cost])
            
        # print avg results in terimnal
        print("AVERAGE RESULTS")
        print("----------------------------------------------------------")
        
        for j in range(len(algos)):
            
            print(f"algo: {names[j]} | district: {district} | avg cost: {sum(cost_shared_list[j])/len(cost_shared_list[j])} | avg iterations: {sum(iterations_list[j])/len(iterations_list[j])} | avg successes: {sum(succes_list[j])/len(succes_list[j])}")

        # print avg results in terimnal
        print("MINIMUM RESULTS")
        print("----------------------------------------------------------")

        for x in range(len(algos)):

            print(f"algo: {names[x]} | district: {district} | min cost: {cost_shared_list[x][index_list[x]]} | iterations: {iterations_list[x][index_list[x]]} | successes: {succes_list[x][index_list[x]]}")
            
if __name__ == "__main__":
    experiment("1", 1, 1)
    #experiment_iterations("1", 1, 1)