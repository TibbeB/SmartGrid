def cable_connection_algorithm(connections: dict[object, list[object]], cables: dict[int, object]) -> None:
    """
    algorithm that randomely connects cables without unique cables
    pre:
    - connections (dict[object, list[object]]): dict that represents state
    - cables (dict[int, object]): dict that represents cables
    post:
    - cables are connected
    """
    
    # loop trough batteries
    for batteries, houses in connections.items():
    
        # list for saving cords of paths
        cables_coordinates_list = []
        
        # loop trough corresponding houses
        for house in houses:
        
            xh = house.x
            yh = house.y
            
            xb = batteries.x
            yb = batteries.y
            
            dx1 = house.x - batteries.x
            dy1 = house.y - batteries.y
            
            da1 = abs(dx1) + abs(dy1)
            da2 = 9999
            
            cable = cables[house.identification]

            xc = cable.x
            yc = cable.y
            
            # loops trough coordinates of already layed segments of cables
            for coordinates in cables_coordinates_list:
                
                # checks distance from house to segments of already layed cable
                tmp_da2 = abs(house.x - coordinates[0]) + abs(house.y - coordinates[1])
                
                # if currently checked segment is closer to house, save that segments coordinates
                if tmp_da2 < da2:
                    da2 = tmp_da2
                    
                    # save coordinates
                    cable_coordinates = (coordinates[0], coordinates[1])
                    
            cables_coordinates_list.append((cable.x, cable.y))
                    
            # if an already layed cable segment is closer than the battery, connect to that segment
            if da2 < da1:

                dx2 = house.x - cable_coordinates[0]
                dy2 = house.y - cable_coordinates[1]
                
                if dx2 < 0:
                    while cable.x < cable_coordinates[0]:
                        cable.right()
                        cables_coordinates_list.append((cable.x, cable.y))
                    
                if dx2 > 0:
                    while cable.x > cable_coordinates[0]:
                        cable.left()
                        cables_coordinates_list.append((cable.x, cable.y))
                        
                if dy2 < 0:
                    while cable.y < cable_coordinates[1]:
                        cable.up()
                        cables_coordinates_list.append((cable.x, cable.y))
                        
                if dy2 > 0:
                    while cable.y > cable_coordinates[1]:
                        cable.down()
                        cables_coordinates_list.append((cable.x, cable.y))
                continue
            
            # else connect to battery
            if dx1 < 0:
                while cable.x < xb:
                    cable.right()
                    cables_coordinates_list.append((cable.x, cable.y))
                    
            if dx1 > 0:
                while cable.x > xb:
                    cable.left()
                    cables_coordinates_list.append((cable.x, cable.y))
                    
            if dy1 < 0:
                while cable.y < yb:
                    cable.up()
                    cables_coordinates_list.append((cable.x, cable.y))
                    
            if dy1 > 0:
                while cable.y > yb:
                    cable.down()
                    cables_coordinates_list.append((cable.x, cable.y))
                        