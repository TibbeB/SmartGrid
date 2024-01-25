from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from hillclimber import hillclimber

import math
from numpy import random

class plant_propagation_algorithm:

    def __init__(self, n_start_runners, N):
        # make population hillclimbers
        self.population = []
        self.costs = []

        for i in range(n_start_runners):
            state = 1
            while state == 1:
                s = Smartgrid("1")
                b, h = s.get_data()
                random_state = random_state_generator(b, h)
                state = make_solution(b, random_state)

            peak_state, cost_climb, iteration = hillclimber(s, N, state, b)
            self.population.append((peak_state, min(cost_climb)))

        print("Population generated")

    def fitness(self): # must be between 0 and 1
        # find max value
        mini = 100000
        for info in self.population:
            if info[1] < mini:
                mini = info[1]

        self.fitness = []
        for info in self.population:
            self.fitness.append(float(mini) / float(info[1]))
        
        print("Fitness calculated")
        print(self.fitness)


    def runners_calc(self, nmax):
        self.n_r = []
        self.N_x = []
        for f_x in self.fitness: 
            self.N_x.append(0.5 * (math.tanh(4 * f_x - 2) + 1))
            self.n_r.append(int(nmax * 0.5 * (math.tanh(4 * f_x - 2) + 1) * random.random()))

        print("n_r calculated")
        print(self.n_r)

    def distance(self):
        for i in self.N_x:
            d = 2*(1 - i)*(random.random() - 0.5) 
            new_N = d * 30000
            print(abs(new_N))





if __name__ == '__main__':
    N = 100 # iterations of initial climb
    nmax = 5
    p = plant_propagation_algorithm(4, N)
    
    fitness_plants = p.fitness()
    p.runners_calc(nmax)
    p.distance()
