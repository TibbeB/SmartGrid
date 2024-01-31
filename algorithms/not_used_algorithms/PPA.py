from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from hillclimber import hillclimber

import math
from numpy import random

class plant_propagation_algorithm:
    
    def __init__(self, n_start_runners, N):
        """Generates a population of hillclimbers

        Pre:
            n_start_runners (int): Size of the first population
            N (int): Initial iterations of the first hillclimbers
        """        
        # make population hillclimbers
        self.population = []
        self.costs = []

        for i in range(n_start_runners):
            state = 1
            while state == 1:
                self.s = Smartgrid("1")
                self.b, h = self.s.get_data()
                random_state = random_state_generator(self.b, h)
                state = make_solution(self.b, random_state)

            peak_state, cost_climb, iteration, succes = hillclimber(self.s, N, state, self.b)
            # state has new batteries
            self.population.append((peak_state, min(cost_climb)))
            print(min(cost_climb))

        print("Population generated")

    def fitness_calc(self):
        """Calculates the fitness of the individual hillclimbers
        """    
        # find max value
        mini = 100000
        for info in self.population:
            if info[1] < mini:
                mini = info[1]

        self.fitness = []
        for info in self.population:
            self.fitness.append(float(mini) / float(info[1]))
        
        print("Fitness calculated")
        print("Fitness:", self.fitness)


    def runners_calc(self, nmax):
        """Calculates Nx value and the number of children each hillclimber gets

        Pre:
            nmax (int): Maximum number of children
        """  

        self.n_r = []
        self.N_x = []
        for f_x in self.fitness: 
            self.N_x.append(0.5 * (math.tanh(4 * f_x - 2) + 1))
            child = int(nmax * 0.5 * (math.tanh(4 * f_x - 2) + 1) * random.random())
            if child == 0:
                self.n_r.append(1)
            
            else:
                self.n_r.append(int(nmax * 0.5 * (math.tanh(4 * f_x - 2) + 1) * random.random()))

        print("n_r calculated")
        print('Number of children', self.n_r)

    def distance_calc(self):
        """Calculates the number of iterations each child gets in a new hillclimber
        """      

        self.travel_distance = []
        for i in self.N_x:
            d = 2*(1 - i)*(random.random() - 0.5) 
            new_N = int(d * 50000)
            self.travel_distance.append(abs(new_N))
        print('distance:',self.travel_distance)

    def new_population(self):
        """Generate new population of hillclimbers
        """        

        for i in range(len(self.population)):
            children = []

            for i in range(self.n_r[i]):
                # wrong batteries are given
                new_batteries = []
                batteries = {}
                for key in self.population[i][0]:
                    new_batteries.append(key)

                for j in range(5):
                    batteries[j] = new_batteries[j]

                peak_state, cost_climb, iteration, succes = hillclimber(self.s, self.travel_distance[i], self.population[i][0], batteries)
                children.append((peak_state, min(cost_climb)))

            highest_child = ('p', 1000000, 's')
            for child in children:
                if child[1] < highest_child[1]:
                    highest_child = child
            
            if not highest_child == ('p', 1000000, 's'):
                self.population[i] = highest_child

        for i in self.population:
            print('costs best child', i[1])
    
    def get_data(self):
        """Returns the data from the class

        Post:
            self.population (list[(dict[object: List[object]], int)]): List that 
                keeps track of the currentpopulation
            state (dict[object: List[object]]): The distribution of houses over the batteries
            min_cost (int): Lowest cost of the final population 
        """        
        min_cost = 100000

        for climber in self.population:
            if climber[1] < min_cost:
                min_cost = climber[1]
                state = climber[0]

        return self.population, state, min_cost


if __name__ == '__main__':
    # Set starting values
    N = 100           
    nmax = 5          
    generations = 7     

    # Make object
    p = plant_propagation_algorithm(4, N)
    
    # Go through steps to make new populations
    for i in range(generations):
        p.fitness_calc()
        p.runners_calc(nmax)
        p.distance_calc()
        p.new_population()

    # Get the data
    population, best_state, min_state = p.get_data()
