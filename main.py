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
        
        self.visualisation(self.batteries, self.houses)
    
    def csv_reader(self, filename_batteries, filename_houses):
        """ initialize objects with csv data"""
        
        # read batteries
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
        
        # read houses
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
        """ extracts cords, capacities and key names from objects in house and battery dicts"""
        
        # create lists
        x_list = []
        y_list = []
        capacity_list = []
        key_list = []
        
        # loop trough objects in dict
        for key, value in dictionary.items():
        
            # return values from objects
            x = value.x
            y = value.y
            capacity = value.capacity
            
            # append values to lists
            x_list.append(x)
            y_list.append(y)
            capacity_list.append(capacity)
            key_list.append(key)
            
        
        return x_list, y_list, capacity_list, key_list
                
    def visualisation(self, batteries_dict, houses_dict):
        """ creates a scatter plot with extracted cords and capacity"""
        
        # extract cords, capacities and key names of objects in house and battery dict
        batteries_list = self.extract_cords_and_capacity(batteries_dict)
        houses_list = self.extract_cords_and_capacity(houses_dict)
        
        # save battery cords and capacity in vars
        x_batteries = batteries_list[0]
        y_batteries = batteries_list[1]
        capacity_batteries = batteries_list[2]
        
        # save house cords and capacity in vars
        x_houses = houses_list[0]
        y_houses = houses_list[1]
        capacity_houses = houses_list[2]
        
        # create scatter plot
        scatter1 = plt.scatter(x_batteries, y_batteries, c=capacity_batteries, s=400, cmap='Blues', edgecolors='black')
        scatter2 = plt.scatter(x_houses, y_houses, c=capacity_houses, s=200, cmap='hot', edgecolors='grey')
        
        # add colorbar
        plt.colorbar(scatter1, label="Capacity batteries")
        plt.colorbar(scatter2, label="Capacity houses")
        
        # label x and y axis
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        
        # add key names to batteries
        for i, key in enumerate(batteries_list[3]):
            plt.annotate(f'({key})', (x_batteries[i], y_batteries[i]),
            textcoords="offset points", xytext=(0, 15), ha='center', fontsize=14, fontweight='bold')
        
        # create grid and show plot
        plt.grid(True, dashes=(1, 1), linewidth=0.5)
        plt.show()
            
if __name__ == "__main__":
    smartgrid = Smartgrid("1")
    