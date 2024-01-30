import json
from objects.battery import Battery
from objects.house import House
from objects.cable import Cable
from quick_plotter import quick_plot

def json_reader(path):

    connections = {}
    
    cables = {}
    
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        
        battery_id = 0
        
        house_id = 0
        
        
        for entry in data:
            
            if 'houses' in entry:
                
                cords_battery = entry["location"].split(',')
                
                x = cords_battery[0]
                
                y = cords_battery[1]
                
                capacity = entry["capacity"]
                
                b = Battery(battery_id, int(x), int(y), float(capacity))
                
                connections[b] = []
                
                battery_id += 1
                
                
                
                for house in entry["houses"]:
                    
                    path_cables_list = []
                    
                    cords_house = entry["location"].split(',')
                    
                    x1 = int(cords_house[0])
                    
                    y1 = int(cords_house[1])
                    
                    output = house["output"]
                    
                    path_cables = house["cables"]
                    
                    for pair in path_cables:
                    
                        tmp = pair.split(',')
                        path_cables_list.append([int(tmp[0]), int(tmp[1])])
                        
                    h = House(house_id, x1, y1, output)
                    
                    connections[b].append(h)
                    
                    c = Cable(h)
                    
                    cables[house_id] = c
                    
                    cables[house_id].path = path_cables_list
                    
                    house_id += 1
                    
    return connections, cables
    
if __name__ == "__main__":

    connections, cables = json_reader("district2_v5_31075$_1s.json")
    
    quick_plot(connections, cables)