from house_distribution import house_distribution
from x_y_path import x_y_path
from hillclimb_not_random import random_switch
from main import Smartgrid

district = "1"
smartgrid = Smartgrid(district)

batteries, houses = smartgrid.get_data

random_state = house_distribution(batteries, houses)

x_y_path(random_state)

random_switch(batteries, random_state)





