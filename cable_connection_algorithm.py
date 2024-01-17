from main import Smartgrid
from random_state_generator import random_state_generator

def cable_connection_algorithm(connections, cables):
    for batteries, houses in connections.items():
    
        
        cables_coordinates_list = []
        
        for house in houses:
            print("-")
        
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
                    
            # if an already layed cable segment is closer than the battery, connect to that segment
            if da2 < da1:

                dx2 = house.x - cable_coordinates[0]
                dy2 = house.y - cable_coordinates[1]
                
                if dx2 < 0:
                    while cable.x < cable_coordinates[0]:
                        print(cable.x, cable_coordinates[0])
                        cable.right()
                        cables_coordinates_list.append((cable.x, cable.y))
                    
                if dx2 > 0:
                    while cable.x > cable_coordinates[0]:
                        print(cable.x, cable_coordinates[0])
                        cable.left()
                        cables_coordinates_list.append((cable.x, cable.y))
                        
                if dy2 < 0:
                    while cable.y < cable_coordinates[1]:
                        print(cable.y, cable_coordinates[0])
                        cable.up()
                        cables_coordinates_list.append((cable.x, cable.y))
                        
                if dy2 > 0:
                    while cable.y > cable_coordinates[1]:
                        print(cable.y, cable_coordinates[0])
                        cable.down()
                        cables_coordinates_list.append((cable.x, cable.y))
                continue
                
            if dx1 < 0:
                while cable.x < xb:
                    print(cable.x, xb)
                    cable.right()
                    cables_coordinates_list.append((cable.x, cable.y))
                    
            if dx1 > 0:
                while cable.x > xb:
                    print(cable.x, xb)
                    cable.left()
                    cables_coordinates_list.append((cable.x, cable.y))
                    
            if dy1 < 0:
                while cable.y < yb:
                    print(cable.y, yb)
                    cable.up()
                    cables_coordinates_list.append((cable.x, cable.y))
                    
            if dy1 > 0:
                while cable.y > yb:
                    print(cable.y, yb)
                    cable.down()
                    cables_coordinates_list.append((cable.x, cable.y))
                        
        print("done")
                
if __name__ == "__main__":
    district = "1"
    smartgrid = Smartgrid(district)

    b, h = smartgrid.get_data()
    
    connections = random_state_generator(b, h)
    
    cable_connection_algorithm(connections, smartgrid.cables)
    
    costs = smartgrid.cost_shared(connections)
    
    smartgrid.json_writer(district, costs, connections)
    
    print(costs)     
    smartgrid.visualisation(b, h)       
                    
               
                
            
