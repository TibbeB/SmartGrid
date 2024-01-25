from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from quick_plotter import quick_plot
from battery_distance import battery_distance
import time
import math
import numpy as np

# v4 adds score to houses based on houses in radius R
# removes some randomness


def cable_connection_v1(connections, cables, R):
    
    for battery, houses in connections.items():
    
        cords_list = [[battery.x, battery.y]]
        
        houses_with_radius_score_list = []
        
        for house1 in houses:
            
            radius_score = 0
            
            for house2 in houses:
            
                distance = math.sqrt( abs(house1.x - house2.x) ** 2 + abs(house1.y -house2.y) ** 2)
                
                if distance < R:
                    radius_score += 1
                    
            houses_with_radius_score_list.append([house1,radius_score])
            
        # so house that is closest to other houses is first in the list
        houses_with_radius_score_list = sorted(houses_with_radius_score_list, key=lambda x: x[1], reverse=True)
        
        for house in houses_with_radius_score_list:
            
            init_absolute_distance = 9999
            
            # find closest cable
            for i in range(len(cords_list)):
                
                absolute_distance = abs(house[0].x - cords_list[i][0]) + abs(house[0].y - cords_list[i][1])
                
                if absolute_distance < init_absolute_distance:
                    
                    init_absolute_distance = absolute_distance
                    
                    saved_x = cords_list[i][0]
                    
                    saved_y = cords_list[i][1]
        
            cable = cables[house[0].identification]
            
            dx = house[0].x - saved_x
            dy = house[0].y - saved_y
            
            cords_list.append([cable.x, cable.y])
            
            # lay cable
            if dx < 0:
                while cable.x < saved_x:
                    cable.right()
                    cords_list.append([cable.x, cable.y])
                
            if dx > 0:
                while cable.x > saved_x:
                    cable.left()
                    cords_list.append([cable.x, cable.y])
                    
            if dy < 0:
                while cable.y < saved_y:
                    cable.up()
                    cords_list.append([cable.x, cable.y])
                    
            if dy > 0:
                while cable.y > saved_y:
                    cable.down()
                    cords_list.append([cable.x, cable.y])
                
if __name__ == "__main__":
    
    start_time = time.time()
    
    def radius_experiment():
        for r in np.arange(11,13,0.1):
        
            costs_list = []
            
            for i in range(100):
                
                district = "1"

                smartgrid = Smartgrid(district)
                
                batteries, houses = smartgrid.get_data()

                invalid_state = random_state_generator(batteries, houses)
                
                valid_state = make_solution(batteries, invalid_state)
                
                if valid_state != 1:
                    
                    cable_connection_v1(valid_state, smartgrid.cables, r)
                        
                    costs = smartgrid.cost_shared(valid_state)
                    
                    costs_list.append(costs)
                    
            print(f"r = {r} - average cost = {sum(costs_list) / len(costs_list)}")
            
    def plot():
    
        district = "1"

        smartgrid = Smartgrid(district)
        
        batteries, houses = smartgrid.get_data()

        invalid_state = battery_distance(batteries, houses)
        
        valid_state = make_solution(batteries, invalid_state)
        
        if valid_state != 1:
            
            cable_connection_v1(valid_state, smartgrid.cables, 20)
            
            cost = smartgrid.cost_shared(valid_state)
            
            print(cost)
            
            quick_plot(valid_state, smartgrid.cables)
            
            
    plot()
    
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Execution time: {elapsed_time} seconds")