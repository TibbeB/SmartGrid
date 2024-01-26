from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
from quick_plotter import quick_plot
from battery_distance import battery_distance
#from cable_connection_algorithm_v4 import cable_connection_v1
import random
import time
import math
import numpy as np
import copy

def len_cables(cables):
    i = 0
    for key, cable in cables.items():
        for items in cable.path:
            i += 1
            
    return i

def cable_connection_hillclimber(connections, cables, N):
    
    
    cords_list1 = []
    
    cords_list2 = []
    
    cords_list3 = []
    
    cords_list4 = []
    
    cords_list5 = []
    
    for battery, houses in connections.items():
        
        identification = battery.identification
        
        for house in houses:
            
            cable = cables[house.identification]
            
            for items in cable.path:
                
                if identification == 0:
                    cords_list1.append([items,house])
                    
                if identification == 1:
                    cords_list2.append([items,house])
                    
                if identification == 2:
                    cords_list3.append([items,house])
                    
                if identification == 3:
                    cords_list4.append([items,house])
                    
                if identification == 4:
                    cords_list5.append([items,house])
                    
    cords_list = [cords_list1, cords_list2, cords_list3, cords_list4, cords_list5]
    
    def cost_shared(dictionary: {object:[object]}) -> int:

        total_cost = 0
        for battery, houses in dictionary.items():
            total_cost += 5000
            for house in houses:
                total_cost += 9 * (len(cables[house.identification].path) - 1)
            
        return total_cost
        
    cost1 = cost_shared(connections)
    
    print(f"cost before = {cost1}")
    
    i = 0
    k = 0
    
    while i < N:
        
        if k > 2000:
            break
            
        random_battery = random.choice(list(connections.keys()))
        
        identification = random_battery.identification
        
        houses = connections[random_battery]

        random_house = random.choice(houses)
        
        cable1 = cables[random_house.identification]
        
        # remove first and last element
        sliced_cable_path = cable1.path[:-1]
        
        saved_cable_path = cable1.path[1:]
        
        check = 0
        
        # to check if other cables originate from this cable
        for item1 in sliced_cable_path:

            for item2 in cords_list[identification]:
            
                if item1 == item2[0]:
                    check = 1
                    break
                    
            if check == 1:
                break
        
        # if so look at different cable
        if check == 1:
            i += 1
            continue
        
        len1 = len(cable1.path)
        
        #print(1, len1)
        
        # clear cable object
        cable1.clear_cable()
        
        # clear list
        to_be_used = []
        
        for item in cords_list[identification]:
            if item[1] != random_house:
                to_be_used.append(item)

        init_absolute_distance = 9999
                
        for k in range(len(to_be_used)):
                
            absolute_distance = abs(random_house.x - to_be_used[k][0][0]) + abs(random_house.y - to_be_used[k][0][1])
            
            if absolute_distance < init_absolute_distance:
                
                init_absolute_distance = absolute_distance
                
                saved_x = to_be_used[k][0][0]
                
                saved_y = to_be_used[k][0][1]
                
                
        dx = random_house.x - saved_x
        dy = random_house.y - saved_y
        
        to_be_used.append([[cable1.x, cable1.y],random_house])
        
        # lay cable
        if dx < 0:
            while cable1.x < saved_x:
                cable1.right()
                to_be_used.append([[cable1.x, cable1.y],random_house])
            
        if dx > 0:
            while cable1.x > saved_x:
                cable1.left()
                to_be_used.append([[cable1.x, cable1.y],random_house])
                
        if dy < 0:
            while cable1.y < saved_y:
                cable1.up()
                to_be_used.append([[cable1.x, cable1.y],random_house])
                
        if dy > 0:
            while cable1.y > saved_y:
                cable1.down()
                to_be_used.append([[cable1.x, cable1.y],random_house]) 
        
        len2 = len(cable1.path)
        
        #print(2,len2)
        
        if len2 < len1:
            print("succes")
            cords_list[identification] = to_be_used
            k = 0
        
        else:
            for item3 in saved_cable_path:
                cable1.path.append(item3)
            k += 1
            
        i += 1
        
    cost2 = cost_shared(connections)
    
    print(f"cost after = {cost2}")
                
if __name__ == "__main__":
    
    start_time = time.time()
    
    def radius_experiment():
        R = 12
        for r in np.arange(1):
        
            costs_list = []
            
            for i in range(100):
                
                district = "1"

                smartgrid = Smartgrid(district)
                
                batteries, houses = smartgrid.get_data()

                invalid_state = battery_distance(batteries, houses)
                
                valid_state = make_solution(batteries, invalid_state)
                
                if valid_state != 1:
                    
                    cable_connection_v1(valid_state, smartgrid.cables, R)
                        
                    costs = smartgrid.cost_shared(valid_state)
                    
                    costs_list.append(costs)
                    
            print(f"- {i} itterations | minimun cost = {min(costs_list)} | radius = {R} | average cost = {sum(costs_list) / len(costs_list)}")
            
    def plot():
    
        district = "1"

        smartgrid = Smartgrid(district)
        
        batteries, houses = smartgrid.get_data()

        invalid_state = battery_distance(batteries, houses)
        
        valid_state = make_solution(batteries, invalid_state)
        
        if valid_state != 1:
            
            cable_connection_v1(valid_state, smartgrid.cables, 20)
            
            cost = smartgrid.cost_shared(valid_state)
            
            print(f"cost = {cost}")
            
            quick_plot(valid_state, smartgrid.cables)
            
            
    #radius_experiment()
    
    #plot()
    
    def debug():
    
        district = "1"

        smartgrid = Smartgrid(district)
        
        batteries, houses = smartgrid.get_data()

        invalid_state = battery_distance(batteries, houses)
        
        valid_state = make_solution(batteries, invalid_state)
        
        if valid_state != 1:
            
            cable_connection_v1(valid_state, smartgrid.cables, 20)
            
            cable_connection_hillclimber(valid_state, smartgrid.cables)
            
            cost = smartgrid.cost_shared(valid_state)

            
    debug()
    
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"- Execution time: {elapsed_time} seconds")