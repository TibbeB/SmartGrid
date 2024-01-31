import copy

def dijkstra(state, cables):
    """
    connects cables via dijkstra method. it works by looking at N houses
    at the first iteration  per battery. than each following iteration looking at N houses again from the N old houses (reference points).
    
    pre:
    - state (dict[object, list[object]]): dict that represents state
    - cables (dict[int, object]): dict that represents cables
    - N (int): represents at how many houses are looked at from each refrence point
    post:
    - cables are connected
    """
    
    N = 3
    
    connections = copy.deepcopy(state)
    
    for battery, houses in connections.items():
        i = 0
        # !! add battery
        removed_houses_list = []
        
        while len(houses) > 0:
            if i == 0:
                cords = [[battery.x, battery.y]]
                
                # list that contains absolute distances in first index and house in second index
                closest_houses = []

                for j, house in enumerate(houses):
                
                    dx = abs(house.x - battery.x)
                    dy = abs(house.y - battery.y)
                    
                    # calculate absolute distance
                    absolute_distance = dx + dy
                    
                    # append absolute distance and house to list
                    closest_houses.append([absolute_distance, house, j])
                
                # sort the list based on the first element of each item in ascending order
                sorted_closest_houses = sorted(closest_houses, key=lambda x: x[0])
                
                # List of N closest houses
                closest_N_houses = sorted_closest_houses[:N]
                
                # remove house from houses and append to removed houses list
                for k in closest_N_houses:
                    removed_houses_list.append(houses.pop(houses.index(k[1])))
                
                # loop trough N closest houses
                for index, pair in enumerate(closest_N_houses):
                
                    # connect closest house to reference point
                    if index == 0:
                        
                        dx = pair[1].x - cords[0][0]
                        dy = pair[1].y - cords[0][1]
                        
                        cable = cables[pair[1].identification]
                        
                        cords.append([cable.x, cable.y])
                        
                        if dx < 0:
                            while cable.x < cords[0][0]:
                                cable.right()
                            
                        if dx > 0:
                            while cable.x > cords[0][0]:
                                cable.left()
                                
                        if dy < 0:
                            while cable.y < cords[0][1]:
                                cable.up()
                                
                        if dy > 0:
                            while cable.y > cords[0][1]:
                                cable.down()
                        
                    # check if other houses are closer than reference point
                    else:
                        
                        for item in cords:
                            
                            # distance to reference point
                            distance_reference = pair[0]
                            
                            # save the distance in var
                            tmp = distance_reference
                            
                            # save reference point cords in vars
                            tmp_x = cords[0][0]
                            tmp_y = cords[0][1]
                            
                            # calculate distance from houses
                            dx1 = pair[1].x - item[0]
                            dy1 = pair[1].y - item[1]
                            
                            d_abs = abs(dx1) + abs(dy1)
                            
                            # if distance to house < distance reference point
                            if d_abs < distance_reference:
                                
                                # save distance and cords
                                tmp = d_abs
                                tmp_x = item[0]
                                tmp_y = item[1]
                            
                        # --------------------------------------------------------
                        # part that moves cables 
                        
                        dx = pair[1].x - tmp_x
                        dy = pair[1].y - tmp_y
                        
                        cable = cables[pair[1].identification]
                        
                        # add cords of newly added house to cords
                        cords.append([cable.x, cable.y])
                        
                        if dx < 0:
                            while cable.x < tmp_x:
                                cable.right()
                            
                        if dx > 0:
                            while cable.x > tmp_x:
                                cable.left()
                                
                        if dy < 0:
                            while cable.y < tmp_y:
                                cable.up()
                                
                        if dy > 0:
                            while cable.y > tmp_y:
                                cable.down()
                        
            else:
                selected_houses = []
                
                for l, removed_house in enumerate(removed_houses_list):
                    
                    # list that contains absolute distances in first index and house in second index
                    closest_houses = []
                    
                    if len(houses) == 0:
                        break
                        
                    for g, house in enumerate(houses):
                    
                        dx = removed_house.x - house.x
                        dy = removed_house.y - house.y
                        
                        abs_d = abs(dx) + abs(dy)
                        
                        closest_houses.append([abs_d, house, g])
                        
                    # sort the list based on the first element of each item in ascending order
                    sorted_closest_houses = sorted(closest_houses, key=lambda x: x[0])

                    # List of N closest houses
                    closest_N_houses = sorted_closest_houses[:N]
                    
                    # remove house from houses and append to removed houses list
                    for k in closest_N_houses:
                        selected_houses.append([k[0], houses.pop(houses.index(k[1]))])
                    
                sorted_selected_houses = sorted(selected_houses, key=lambda x: x[0])    
                        
                for hou in sorted_selected_houses:
                
                    for h in removed_houses_list:
                        dx = hou[1].x - h.x
                        dy = hou[1].y - h.y
                        abs_d = abs(dx) + abs(dy)
                        
                        tmp_d = 9999
                        
                        if abs_d < tmp_d:
                            tmpg = abs_d
                            tmpd_x = h.x
                            tmpd_y = h.y
                        
                    dx = hou[1].x - tmpd_x
                    dy = hou[1].y - tmpd_y
                    
                    cable = cables[hou[1].identification]
                    
                    removed_houses_list.append(hou[1])
                    
                    if dx < 0:
                        while cable.x < tmpd_x:
                            cable.right()
                        
                    if dx > 0:
                        while cable.x > tmpd_x:
                            cable.left()
                            
                    if dy < 0:
                        while cable.y < tmpd_y:
                            cable.up()
                            
                    if dy > 0:
                        while cable.y > tmpd_y:
                            cable.down()                        
                        
            i += 1
            