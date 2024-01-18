from house_distribution import house_distribution
from x_y_path import x_y_path
from main import Smartgrid

import matplotlib.pyplot as plt
import tkinter
import matplotlib
matplotlib.use('TkAgg')

district = "2"
N = 10000

random_states_list = []

for i in range(N):
    smartgrid = Smartgrid(district)

    batteries, houses = smartgrid.get_data()

    random_state = house_distribution(batteries, houses)

    smartgrid.x_y_path(random_state)
    
    random_states_list.append(smartgrid.cost_shared(random_state))
    
multiplier = [0] * len(random_states_list)

for i in range(len(random_states_list)):
    for j in range(i+1, len(random_states_list)):
        if random_states_list[j] == random_states_list[i]:
            multiplier[i] += 1

            
plt.scatter(random_states_list, multiplier)
plt.show()





