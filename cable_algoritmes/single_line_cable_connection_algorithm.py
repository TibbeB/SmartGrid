import copy

def single_line_cable_connection_algorithm(state: dict[object,list[object]], cables: dict[int, object]) ->:
     """
    connects cables via dijkstra method. it works by looking at N houses
    at the first iteration  per battery. than each following iteration looking at N houses again from the N old houses (reference points).
    
    pre:
    - state (dict[object, list[object]]): dict that represents state
    - cables (dict[int, object]): dict that represents cables
    post:
    - cables are connected
    """
    connections = copy.deepcopy(state)
    
    for battery, houses in connections.items():
        
        cord_list = [[battery.x, battery.y]]
        
        # runs until all houses are connected
        while len(houses) > 0:
            
            # init distance
            distance = 9999
            
            for index, house in enumerate(houses):
            
                # calculate absolute distance
                dx = abs(house.x - cord_list[-1][0])
                dy = abs(house.y - cord_list[-1][1])
                tmp = dx + dy
                
                # check if current distance is less than old distance
                if tmp < distance:
                    
                    # save current distance
                    distance = tmp
                    
                    # save corresponding object
                    first_house = house
                    
                    # save index of house
                    save_index = index
            
            # calculate how many steps in x and y direction should be taken
            dx1 = first_house.x - cord_list[-1][0]
            dy1 = first_house.y - cord_list[-1][1]
            
            # get cable corresponding to house
            cable = cables[house.identification]
            
            # if current house is left of reference point
            if dx1 < 0:
                while cable.x < cord_list[-1][0]:
                    cable.right()
            
            # if current house is right of reference point            
            if dx1 > 0:
                while cable.x > cord_list[-1][0]:
                    cable.left()
            
            # if current house is below of reference point  
            if dy1 < 0:
                while cable.y < cord_list[-1][1]:
                    cable.up()
            
            # if current house is above of reference point  
            if dy1 > 0:
                while cable.y > cord_list[-1][1]:
                    cable.down()
            
            # create new reference point
            cord_list.append([first_house.x, first_house.y])
            
            # remove current house from houses list
            houses.pop(save_index)
            
    