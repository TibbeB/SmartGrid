import random

# v5 cables run to centers of busy areas
def draw_cables(dx, dy, saved_x, saved_y, cords_list, cable):
    """
    lays a path from (dx,dy) to (saved_x,saved_y) using manhattan distance
    
    pre:
    - dx (int): begin x
    - dy (int): begin y
    - saved_x (int): end x
    - saved_y (int): end y
    - cords_list (list[int, int]): list of previously visited cords
    - cable (dict[int, object]): cables dict
    post:
    - cables are drawn
    """

    cords_list.append([cable.x, cable.y])
            
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
            
def draw_closest_cables(cords_list, cables, house):
    """
    use previously visited cords list to draw cable to nearest cable
    
    pre:
    - cords_list (list[int, int]): list of previously visited cords
    - cables (dict[int, object]): cables dict
    - house (object): house object

    """
    
    init_absolute_distance = 9999
    
    # find closest path
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

def cable_connection_v1(connections, cables):
    """
    algorithm that randomely connects cables without unique cables
    pre:
    - connections (dict[object, list[object]]): dict that represents state
    - cables (dict[int, object]): dict that represents cables
    post:
    - cables are connected
    """

    grid_cords = []
    
    for i in range(50):
        for j in range(50):
            grid_cords.append([i,j])
            
    for battery, houses in connections.items():
        
        cords_list = [[battery.x,battery.y]]
        
        scores_list = []
        
        # add scores to grid cords
        for index, item in enumerate(grid_cords):
            
            score = 0
            
            for house in houses:

                distance = abs(item[0] - house.x) + abs(item[1] - house.y)
                
                score += distance
            
            scores_list.append([score,index])
            
        sorted_scores_list = sorted(scores_list)
        
        # find closest house to best grid cord
        for index1, score1 in enumerate(sorted_scores_list):
            
            init_absolute_distance = 9999
            
            for house in houses:
            
                absolute_distance = abs(grid_cords[score1[1]][0] - house.x) + abs(grid_cords[score1[1]][1] - house.y)
                
                if absolute_distance < init_absolute_distance:
                    
                    saved_x = grid_cords[score1[1]][0]
                    
                    saved_y = grid_cords[score1[1]][1]
                    
                    init_absolute_distance = absolute_distance
                    
                    closest_house = house
                    
            if index1 != 0:
                break
            
        dx = saved_x - battery.x
        dy = saved_y - battery.y
        
        cable = cables[closest_house.identification]
        
        # draw from battery to best grid cord
        draw_cables(dx, dy, battery.x, battery.y, cords_list, cable)
        
        # draw from best grid cord to closest house:
        draw_closest_cables(cords_list, cables, closest_house)
        
        # houses list without closest house to best grid cord
        cleared_houses = []
        
        for item in houses:
            if item != closest_house:
                cleared_houses.append(item)
        
        houses_with_score_list = []
    
        # add scores to houses where score: sum of distances from other houses
        for house1 in cleared_houses:
            score = 0
            
            for house2 in cleared_houses:
            
                score += abs(house1.x - house2.x) + abs(house1.y - house2.y)
                   
            houses_with_score_list.append([house1,score])
        
        # so house that is closest to other houses is first in the list
        houses_with_score_list = sorted(houses_with_score_list, key=lambda x: x[1])
        
        # draw remaining cables
        for house3 in houses_with_score_list:
            draw_closest_cables(cords_list, cables, house3[0])
                