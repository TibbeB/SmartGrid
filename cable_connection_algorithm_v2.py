from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from quick_plotter import quick_plot
import time


# v2 adds score to houses where score: sum of distances from other houses
# the lower the score the better
# introduces unique solution for each state since randomness is removed

def cable_connection_v1(connections, cables):
    
    for battery, houses in connections.items():
    
        cords_list = [[battery.x, battery.y]]
        
        houses_with_score_list = []
        
        # add scores to houses where score: sum of distances from other houses
        for house1 in houses:
            score = 0
            
            for house2 in houses:
            
                score += abs(house1.x - house2.x) + abs(house1.y - house2.y)
                   
            houses_with_score_list.append([house1,score])
        
        # so house that is closest to other houses is first in the list
        houses_with_score_list = sorted(houses_with_score_list, key=lambda x: x[1])
        
        for house in houses_with_score_list:
            
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
    
    costs_list = []
    
    def experiment():
        for i in range(100):
            
            district = "1"

            smartgrid = Smartgrid(district)
            
            batteries, houses = smartgrid.get_data()

            invalid_state = random_state_generator(batteries, houses)
            
            valid_state = make_solution(batteries, invalid_state)
            
            if valid_state != 1:
                
                cable_connection_v1(valid_state, smartgrid.cables)
                    
                costs = smartgrid.cost_shared(valid_state)
                
                costs_list.append(costs)
                
        print(sum(costs_list) / len(costs_list))
        
    def plot():
        district = "3"

        smartgrid = Smartgrid(district)
        
        batteries, houses = smartgrid.get_data()

        invalid_state = random_state_generator(batteries, houses)
        
        valid_state = make_solution(batteries, invalid_state)
        
        if valid_state != 1:
            
            cable_connection_v1(valid_state, smartgrid.cables)
            
            costs = smartgrid.cost_shared(valid_state)
            
            print(costs)
            
            quick_plot(valid_state, smartgrid.cables)
    
    plot()
    
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Execution time: {elapsed_time} seconds")