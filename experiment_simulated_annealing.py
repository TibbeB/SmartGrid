from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from cable_connection_algorithm import cable_connection_algorithm
from hillclimber import random_switch

import matplotlib.pyplot as plt
from numpy import random
import math
import time

def prob(old, new, temp):
    exponent = (old - new) / temp
    if exponent > 700: 
        return 0
    else:
        return math.pow(2, exponent)


def simulated_annealing(max_time, state, b, T, slope, cable_connection_algorithm,s, cable_connection_algorithm_name):
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

if __name__ == '__main__':
    # make state
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

    # print(iteration)
    print(min(cost_climb))
    plt.plot(iteration, cost_climb)
    plt.savefig("simulated_annealing.png")
    plt.show()