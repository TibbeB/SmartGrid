# import fucntions from different files
from random_state_generator import random_state_generator
from FFD import x_y_path
from main import Smartgrid
from cable_connection_algorithm import cable_connection_algorithm
from random_solution import make_solution

# imports to plot 
import matplotlib.pyplot as plt
import tkinter
import matplotlib
matplotlib.use('TkAgg')

# set district variable
district = "1"

# number of random states to generate
N = 400

# cost list of gererated states
random_states_list = []

unique_state_list = []

for i in range(N):

    # create smartgrid instance
    smartgrid = Smartgrid(district)
    
    # get battery and house objects
    batteries, houses = smartgrid.get_data()

    # generate random state
    random_state = random_state_generator(batteries, houses)
    
    solution_state = make_solution(batteries, random_state)
    
    if solution_state == 1:
        continue
        
    # connect paths
    cable_connection_algorithm(solution_state, smartgrid.cables)
    
    unique_state_list.append(solution_state)
    
    # append random state cost to random_states_list
    random_states_list.append(smartgrid.cost_shared(random_state))

id_occupied_capacities = [] 

identification = 0
for state in unique_state_list:

    token_string = ""
    
    for battery in state:
    
        token_string += f"{battery.occupied_capacity}"
        
    dot_free_token_string = token_string.replace(".","")
    
    identification += 1
    
    id_occupied_capacities.append([identification, int(dot_free_token_string)])
   
id_list = []   
for i in range(len(id_occupied_capacities)):
    for j in range(i+1,len(id_occupied_capacities)):
        if id_occupied_capacities[i][1] == id_occupied_capacities[j][1]:
            id_occupied_capacities[j][0] = id_occupied_capacities[i][0]
            
    id_list.append(id_occupied_capacities[i][0])
   
plt.hist(id_list, bins=400)

plt.xlabel('State')
plt.ylabel('Frequency')

plt.savefig('baseline.png')
plt.show()





