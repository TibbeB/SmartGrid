# import fucntions from different files
from random_state_generator import random_state_generator
from FFD import x_y_path
from main import Smartgrid
from cable_connection_algorithm import cable_connection_algorithm

# imports to plot 
import matplotlib.pyplot as plt
import tkinter
import matplotlib
matplotlib.use('TkAgg')

# set district variable
district = "1"

# number of random states to generate
N = 10000

# cost list of gererated states
random_states_list = []

for i in range(N):

    # create smartgrid instance
    smartgrid = Smartgrid(district)
    
    # get battery and house objects
    batteries, houses = smartgrid.get_data()

    # generate random state
    random_state = random_state_generator(batteries, houses)
    
    # connect paths
    cable_connection_algorithm(random_state, smartgrid.cables)
    
    # append random state cost to random_states_list
    random_states_list.append(smartgrid.cost_shared(random_state))


# list to store the frequency of each unique random state
multiplier = [0] * len(random_states_list)

# count the frequency of each unique random state
for i in range(len(random_states_list)):
    for j in range(i+1, len(random_states_list)):
        if random_states_list[j] == random_states_list[i]:
            multiplier[i] += 1

# scatter plot of random state costs against their frequencies
plt.scatter(random_states_list, multiplier)
plt.show()





