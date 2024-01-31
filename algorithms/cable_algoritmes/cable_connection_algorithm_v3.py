import random

# v3
# randomness is reintroduced
# battery - house connections will be layed for houses below certain score S

def cable_connection_v1(connections: dict[object, list[object]], cables: dict[int, object]) -> None:
    """
    algorithm that randomely connects cables without unique cables
    pre:
    - connections (dict[object, list[object]]): dict that represents state
    - cables (dict[int, object]): dict that represents cables
    post:
    - cables are connected
    """
    
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
        
        S = 500
        
        counter = 0
        
        # connect with battery
        for house in houses_with_score_list:
        
            if house[1] < S:
                
                cable = cables[house[0].identification]
            
                dx = house[0].x - battery.x
                dy = house[0].y - battery.y
                
                cords_list.append([cable.x, cable.y])
                
                # lay cable
                if dx < 0:
                    while cable.x < battery.x:
                        cable.right()
                        cords_list.append([cable.x, cable.y])
                    
                if dx > 0:
                    while cable.x > battery.x:
                        cable.left()
                        cords_list.append([cable.x, cable.y])
                        
                if dy < 0:
                    while cable.y < battery.y:
                        cable.up()
                        cords_list.append([cable.x, cable.y])
                        
                if dy > 0:
                    while cable.y > battery.y:
                        cable.down()
                        cords_list.append([cable.x, cable.y])
                    
                houses_with_score_list.remove(house)
                
                counter += 1
        
        if counter > 0:
            random.shuffle(houses_with_score_list)
        
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
                