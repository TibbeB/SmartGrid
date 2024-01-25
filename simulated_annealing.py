from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from cable_connection_algorithm import cable_connection_algorithm
from hillclimber import random_switch

import matplotlib.pyplot as plt
from numpy import random

def prob(old, new, temp):
    return 2**((old - new) / temp)


def simulated_annealing(N, state, b, T):
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

    # Make small changes
    for i in range(N):
        print(i)

        # clear cables
        for key, cable in s.cables.items():
            cable.clear_cable()

        # calculate the cost of the new state
        new_state = random_switch(b, state)
        cable_connection_algorithm(new_state, s.cables)
        new_cost = s.cost_shared(new_state)

        climb.append(new_cost)
        iteration.append(i + 1)
        if prob(cost, new_cost, temp) < 1:
            probs.append(prob(cost, new_cost, temp))
            iteration_prob.append(i)
        # check if new state is better
        if random.random() < prob(cost, new_cost, temp):
            state = new_state

            if cost > new_cost:
                cost = new_cost
            
            new_batteries = []
            for key in state:
                new_batteries.append(key)

            for i in range(5):
                b[i] = new_batteries[i]

        # temp = T - (T / N) * i
        temp = T * 0.997**i
        ts.append(temp)

    # cable_connection_algorithm(state, s.cables)
    # s.visualisation(b, h)

    plt.plot(iteration, ts)
    plt.show()

    plt.plot(iteration_prob, probs)
    print(len(ts))
    plt.show()


    return state, climb, iteration

if __name__ == '__main__':
    # make state
    state = 1
    while state == 1:
        s = Smartgrid("1")
        b, h = s.get_data()
        random_state = random_state_generator(b, h)
        state = make_solution(b, random_state)
    
    # hillclimb
    N = 2500
    T = 1000
    peak_state, cost_climb, iteration = simulated_annealing(N, state, b, T)

    # print(iteration)
    # print(cost_climb)
    plt.plot(iteration, cost_climb)
    plt.savefig("hillclimb.png")
    plt.show()