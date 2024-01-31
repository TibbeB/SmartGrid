from experiment_hillclimber import random_switch
from numpy import random
import math
import time

def prob(old, new, temp):
    """calculates the probability 

    Args:
        old (int): Old cost
        new (int): New cost
        temp (int): Current temperature

    Returns:
        int: The probability
    """  
    exponent = (old - new) / temp
    if exponent > 700: 
        return 0
    else:
        return math.pow(2, exponent)


def simulated_annealing(max_time, state, b, T, slope, cable_connection_algorithm, s, cable_connection_algorithm_name):
    """_summary_

    Args:
        max_rime (int): time hillclimber runs
        state (dict[object: list[object]]): The distribution of houses over the batteries
        b (dict[int: object]): List of the battery objects
        T (int): Starting temperature
        slope (int): 'slope' of the temperature function
        cable_connection_algorithm (Callable[dict[object, list[object]]): cable connection fucntion
        s (Smartgrid): smartgrid instance
        cable_connection_algorithm_name (str): name of cable connection algo

    Returns:
        state (dict[object: list[object]]): The distribution of houses over the batteries
        climb (list[int]): List of the costs of all the states generated in the hillclimber
        iteration (list[int]): List of corresponding iteration to to costs in climb
        
    """ 
    # make lists for to store data
    climb = []
    iteration = []
    iteration_prob = []
    probs = []
 
    # Set start point of the climb
    cable_connection_algorithm(state, s.cables)
    cost = s.cost_shared(state)
    climb.append(cost)
    iteration.append(0)

    ts = []
    ts.append(T)
    temp = T
    
    start = time.time()
    
    j = 0
    i = 0
    # Make small changes
    while time.time() - start < max_time:
        climb.append(cost)
        iteration.append(i + 1)
        
        # clear cables
        for key, cable in s.cables.items():
            cable.clear_cable()

        # calculate the cost of the new state
        new_state = random_switch(b, state)
        cable_connection_algorithm(new_state, s.cables)
        new_cost = s.cost_shared(new_state)

        if prob(cost, new_cost, temp) < 1:
            probs.append(prob(cost, new_cost, temp))
            iteration_prob.append(i)

        # accept new state based on prob()
        if random.random() < prob(cost, new_cost, temp):
            state = new_state
            cost = new_cost
            
            new_batteries = []
            for key in state:
                new_batteries.append(key)

            for i in range(5):
                b[i] = new_batteries[i]
        
        print(f"hillclimber | cable connection algo: {cable_connection_algorithm_name} | run: {j}")        
        
    
        # temp = T - (T / N) * i
        temp = T * slope**i
        ts.append(temp)
        
        j += 1
        i += 1
        
    return state, climb, j


