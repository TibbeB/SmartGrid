random_path(self):
    """connect cables from houses to batteries
    
    pre:
    - dict_connections is a dict
    - csv_reader is called
    - even_distribution is called
    
    post:
    - all houses are connected to batteries"""

    # iterates trough all batteries in the dictionaries
    for battery in dict_connections:
        x_battery = battery.x
        y_battery = battery.y
        
        connections = dict_connections[battery]

        # iterates trough all houses at a specific battery
        for houses in connections:
            cable = self.cables[houses.identification]

            x_house = houses.x
            y_house = houses.y
            
            x_distance = x_battery - x_house
            y_distance = y_battery - y_house
            
            # iterates trough all steps from the house to the battery
            # determines left or right
            for x_steps in range(abs(x_distance)):
                if x_distance < 0:
                    cable.left()
                    
                else:
                    cable.right()
            
            # iterates trough all steps from the house to the battery
            # determines up or down
            for y_steps in range(abs(y_distance)):
                if y_distance < 0:
                    cable.down()
                    
                else:
                    cable.up()