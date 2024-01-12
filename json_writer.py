
def json_writer(self, district, cost_shared, dictionary, cables_dict):
    # create empty data list
    data = []
    
    # first entry
    entry1 = {"district": district, "cost-shared": cost_shared}
    data.append(entry1)
    
    # loop to create remaining entries
    for battery, houses in dictionary.items():
    
        # create battery entry
        entry = {"location": f"{battery.x},{battery.y}", "capacity": battery.capacity,"houses": []}
 
        # loop for filling "houses" key of current battery entry
        for house in houses:
   
            string_path_cords = []
            
            # turn path cords into string
            for cords in cables_dict[house.identification].path:
                string = f"{cords[0]},{cords[1]}"
                string_path_cords.append(string)
            
            # create house_entry
            house_entry = {"location": f"{house.x, house.y}", "output": house.capacity, "cables": string_path_cords}
            
            # append hous_entry to "houses" key 
            entry["houses"].append(house_entry)
            
        # append battery entry to data
        data.append(entry)     
    
    # create json file containing "data"
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)
   