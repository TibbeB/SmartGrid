from battery import Battery
from house import House
import csv
import pandas as pd
import matplotlib.pyplot as plt
import tkinter
import matplotlib
matplotlib.use('TkAgg')


class Smartgrid():

    def __init__(self, district):
        
        self.batteries = {}
        self.houses = {}
        
        filename_batteries = f"Huizen&Batterijen/district_{district}/district-{district}_batteries.csv"
        filename_houses = f"Huizen&Batterijen//district_{district}/district-{district}_houses.csv"
        
        self.csv_reader(filename_batteries, filename_houses)
        
        self.visualisation()
    
    def csv_reader(self, filename_batteries, filename_houses):
        """ initializes objecten met csv data"""
    
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
                
    def extract_cords_and_capacity(self, dictionary):
        """ extracts cords and capacity from house or battery objects"""
        x_list = []
        y_list = []
        capacity_list = []
        
        for key, value in dictionary.items():
            x = value.x
            y = value.y
            capacity = value.capacity
            
            x_list.append(x)
            y_list.append(y)
            capacity_list.append(capacity)
        
        return x_list, y_list, capacity_list
                
    def visualisation(self):
        """ creates a scatter plot with extracted cords and capacity"""
        
        self.batteries_lijst = self.extract_cords_and_capacity(self.batteries)
        self.houses_lijst = self.extract_cords_and_capacity(self.houses)
        
        x_batteries = self.batteries_lijst[0]
        y_batteries = self.batteries_lijst[1]
        
        x_houses = self.houses_lijst[0]
        y_houses = self.houses_lijst[1]
        
        plt.scatter(x_batteries, y_batteries)
        plt.scatter(x_houses, y_houses)
        
        plt.grid(True, dashes=(1, 1), linewidth=0.5)
        plt.show()
            
if __name__ == "__main__":
    smartgrid = Smartgrid("1")
    