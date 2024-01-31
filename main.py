from FFD import even_distribution, x_y_path

from objects.battery import Battery
from objects.house import House
from objects.cable import Cable

import csv
import pandas as pd
import matplotlib.pyplot as plt
import tkinter
import matplotlib
import json
import numpy as np
matplotlib.use('TkAgg')


class Smartgrid():

    def __init__(self, district):
        
        self.batteries = {}
        self.houses = {}
        self.cables = {}
        
        filename_batteries = f"Huizen&Batterijen/district_{district}/district-{district}_batteries.csv"
        filename_houses = f"Huizen&Batterijen//district_{district}/district-{district}_houses.csv"
        
        self.csv_reader(filename_batteries, filename_houses)
        
        # self.visualisation(self.batteries, self.houses)
    
    def csv_reader(self, filename_batteries: str, filename_houses: str) -> None:
        """ initialize objects with csv data
        
        pre:
        - filename_batteries is a str
        - filename_houses is a str
        
        post:
        - self.batteries, self.houses and self.cables are filled with objects"""
        
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
                
                # create battery object
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
                
                # create house object
                self.houses[house_id] = House(house_id, int(x), int(y), float(capacity))
                
                # create cable object
                self.cables[house_id] = Cable(self.houses[house_id])

                house_id += 1
                
    def extract_cords_and_capacity(self, dictionary: dict) -> list:
        """ extracts cords, capacities and key names from objects in house and battery dicts
        
        pre: 
        - dictionary is a dict
        
        post:
        - returns 4 list containing key names(1), cords(2) and capcities(1)"""
        
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
                
    def visualisation(self, batteries_dict: dict, houses_dict: None) -> None:
        """ creates a scatter plot with extracted cords and capacity
        
        pre:
        - batteries_dict is a dict
        - houses_dict is a dict
        - csv_reader is called
        - even_distribution is called
        - x_y_path is called
        
        post:
        - a plot of the state is generated and displayed"""
        
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

        # draw cables
        for key, cable in self.cables.items():
            x = []
            y = []

            for coordinate in cable.path:
                x.append(coordinate[0])
                y.append(coordinate[1])

            plt.plot(x, y, color = 'b')
        
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
        plt.savefig("1.png")
        plt.show()

    def x_y_path(self, dict_connections: {object:[object]}) -> None:
        x_y_path(self, dict_connections)
        
    def cost_shared(self, dictionary: {object:[object]}) -> int:
        """calculates total cost of state
        
        pre:
        - dictionary is a dict
        - csv_reader is called
        - even_distribution is called
        - x_y_path is called
        
        post:
        - total cost is returned as int: total_cost"""
        
        total_cost = 0
        for battery, houses in dictionary.items():
            total_cost += 5000
            for house in houses:
                total_cost += 9 * (len(self.cables[house.identification].path) - 1)
            
        return total_cost

    def json_writer(self, district: str, cost_shared: int, dictionary: {object:[object]}) -> None:
        """ creates json file
        
        pre:
        - district is a str
        - cost_shared is a int
        - dictionary is a dict
        - csv_reader is called
        - even_distribution is called
        - x_y_path is called
        
        post:
        - json file is created and saved to SmartGrid folder"""
        
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
                for cords in self.cables[house.identification].path:
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

    def get_data(self) -> dict:
        """returns batteries and houses dicts
        
        pre:
        - csv_reader is called
        
        post:
        - returns self.batteries and self.houses"""
        
        return self.batteries, self.houses
            

    

    