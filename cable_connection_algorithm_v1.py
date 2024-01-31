from main import Smartgrid
from random_state_generator import random_state_generator
from random_solution import make_solution
import time

def cable_connection_v1(connections: dict[object, list[object]], cables: dict[int, object]) -> None:
    """
    algorithm that randomely connects cables without unique cables
    pre:
    - connections (dict[object, list[object]]): dict that represents state
    - cables (dict[int, object]): dict that represents cables
    post:
    - cables are connected
    """
    
    # loop trough batteries
    for battery, houses in connections.items():
    
        cords_list = [[battery.x, battery.y]]
        
        # loop trough houses corresponding to batteries
        for house in houses:
            
            
            init_absolute_distance = 9999
            
            # find closest cable
            for i in range(len(cords_list)):
                
                absolute_distance = abs(house.x - cords_list[i][0]) + abs(house.y - cords_list[i][1])
                
                if absolute_distance < init_absolute_distance:
                    
                    init_absolute_distance = absolute_distance
                    
                    saved_x = cords_list[i][0]
                    
                    saved_y = cords_list[i][1]
        
            cable = cables[house.identification]
            
            dx = house.x - saved_x
            dy = house.y - saved_y
            
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
    
    for i in range(1):
        
        district = "3"

        smartgrid = Smartgrid(district)
        
        batteries, houses = smartgrid.get_data()

        invalid_state = random_state_generator(batteries, houses)
        
        valid_state = make_solution(batteries, invalid_state)
        
        if valid_state != 1:
            
            cable_connection_v1(valid_state, smartgrid.cables)
                
            costs = smartgrid.cost_shared(valid_state)
            
            costs_list.append(costs)
            
    print(sum(costs_list) / len(costs_list))
    
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Execution time: {elapsed_time} seconds")
        
