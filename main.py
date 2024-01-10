from battery import Battery
from house import House
import csv

class Smartgrid():

    def __init__(self, district):
    
        self.batteries = {}
        self.houses = {}
        
        filename_batteries = f"Huizen&Batterijen/district_{district}/district-{district}_batteries.csv"
        filename_houses = f"Huizen&Batterijen//district_{district}/district-{district}_houses.csv"
        
        self.inlezer(filename_batteries, filename_houses)

    def inlezer(self, filename_batteries, filename_houses):
    
        with open(filename_batteries, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            battery_id = 0
            for line in csv_reader:
                coordinates = line[0].split(',')
                x = coordinates[0]
                y = coordinates[1]
                capacity = line[1]
                self.batteries[battery_id] = Battery(battery_id, int(x), int(y), float(capacity))
                battery_id += 1
                    
        with open(filename_houses, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            house_id = 0
            for line in csv_reader:
                x = line[0]
                y = line[1]
                capacity = line[2]
                self.houses[house_id] = House(battery_id, int(x), int(y), float(capacity))
                house_id += 1
            
if __name__ == "__main__":
    smartgrid = Smartgrid("1")
    