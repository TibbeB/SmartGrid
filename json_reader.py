import json
from algorithms.initial_state_algorithms.objects.battery import Battery
from algorithms.initial_state_algorithms.objects.house import House
from algorithms.initial_state_algorithms.objects.cable import Cable


def json_reader(path: str) -> tuple[dict[object, list[object]], dict[int, object]]:
    """
    reconverts json file representing state into dictionary.
    uou can use the function quick_plot to create visualisation of the state
    
    pre:
    - path (str): represents path to json file
    post:
    - returns connections (dict[object, list[object]]): state represented in dict
    - returns cables (dict[int, object]): cables dict
    """
    connections = {}
    
    cables = {}
    
    # open json file
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        battery_id = 0
        
        house_id = 0
        
        
        for entry in data:
            
            # only read entry if it represents a battery
            if 'houses' in entry:
                
                cords_battery = entry["location"].split(',')
                
                x = cords_battery[0]
                
                y = cords_battery[1]
                
                capacity = entry["capacity"]
                
                # create battery object
                b = Battery(battery_id, int(x), int(y), float(capacity))
                
                connections[b] = []
                
                battery_id += 1
                
                
                # loop trough houses list
                for house in entry["houses"]:
                    
                    path_cables_list = []
                    
                    cords_house = entry["location"].split(',')
                    
                    x1 = int(cords_house[0])
                    
                    y1 = int(cords_house[1])
                    
                    output = house["output"]
                    
                    # read cable path 
                    path_cables = house["cables"]
                    
                    # turn x and y cords of cable path into list of ints
                    for pair in path_cables:
                    
                        tmp = pair.split(',')
                        path_cables_list.append([int(tmp[0]), int(tmp[1])])
                    
                    # create house object
                    h = House(house_id, x1, y1, output)
                    
                    connections[b].append(h)
                    
                    # create cable object
                    c = Cable(h)
                    
                    cables[house_id] = c
                    
                    # append path to cable
                    cables[house_id].path = path_cables_list
                    
                    house_id += 1
                    
    return connections, cables