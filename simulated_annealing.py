from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from cable_connection_algorithm import cable_connection_algorithm
from hillclimber import random_switch

import matplotlib.pyplot as plt
from numpy import random
import math

def prob(old, new, temp):
    """calculates the probability 

    Pre:
        old (int): Old cost
        new (int): New cost
        temp (int): Current temperature

    Post:
        int: The probability
    """    
    exponent = (old - new) / temp
    if exponent > 700: 
        return 1.1
    else:
        return math.pow(2, exponent)


def simulated_annealing(N, state, b, T, slope):
    """_summary_

    Pre:
        N (int): Number of times the hillclimber switches two houses
        state (dict[object: list[object]]): The distribution of houses over the batteries
        b (dict[int: object]): List of the battery objects
        T (int): Starting temperature
        slope (int): 'slope' of the temperature function

    Post:
        state (dict[object: list[object]]): The distribution of houses over the batteries
        climb (list[int]): List of the costs of all the states generated in the hillclimber
        iteration (list[int]): List of corresponding iteration to to costs in climb
        
    """    
    # Make lists to store data
    climb = []
    iteration = []
    iteration_prob = []
    probs = []
    ts = []
 
    # Set start point of the climb
    cable_connection_algorithm(state, s.cables)
    cost = s.cost_shared(state)
    climb.append(cost)
    iteration.append(0)

    # Set start temperature
    ts.append(T)
    temp = T

    # Make small changes
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
        cable_connection_algorithm(new_state, s.cables)
        new_cost = s.cost_shared(new_state)

        # Keep track of the calculated probabilities for visualisation
        if prob(cost, new_cost, temp) <= 1:
            probs.append(prob(cost, new_cost, temp))
            iteration_prob.append(i)

        # Accept new state based on prob()
        if random.random() < prob(cost, new_cost, temp):
            state = new_state
            cost = new_cost
            
            new_batteries = []
            for key in state:
                new_batteries.append(key)

            for i in range(5):
                b[i] = new_batteries[i]

        # Calculate new temperature
        temp = T * slope**i
        ts.append(temp)

    # Visualisation of temperture function and calculated probabilities 
    plt.plot(iteration, ts)
    plt.show()

    plt.plot(iteration_prob, probs)
    print(len(ts))
    plt.show()

    return state, climb, iteration

if __name__ == '__main__':
    # Make state
    state = 1
    while state == 1:
        s = Smartgrid("1")
        b, h = s.get_data()
        random_state = random_state_generator(b, h)
        state = make_solution(b, random_state)
    
    # simulated anneal
    N = 1000
    T = 40
    slope = 0.994
    peak_state, cost_climb, iteration = simulated_annealing(N, state, b, T, slope)

    # Visualisation
    print(min(cost_climb))
    plt.plot(iteration, cost_climb)
    plt.show()