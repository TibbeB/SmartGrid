from main import Smartgrid
from random_state_generator import random_state_generator
from FFD import x_y_path
from numpy import random
import numpy as np

def heuraka(occupied_c, capacities):
    for i in range(len(capacities)):
        if occupied_c[i] > capacities[i]:
            return False
    return True

def make_solution(batteries, connections):
    occupied_c = []
    capacities = []
    for key, battery in batteries.items():
        occupied_c.append(battery.occupied_capacity)
        capacities.append(battery.capacity)

    # make new(/better) state by switching 1 or 2 house(s)
    j = 0
    tries = 0
    while not heuraka(occupied_c, capacities):
        j += 1
        p = random.uniform(0, 1)
        
        # Switch one house
        if p < 0.15:
            while True:
                tries += 1
                
                if tries > 1000:
                    break

                # Select battery
                battery_1, battery_2 = 0, 0
                while battery_1 == battery_2:
                    index_b1 = random.choice([0, 1, 2, 3, 4])
                    index_b2 = random.choice([0, 1, 2, 3, 4])
                    battery_1 = batteries[index_b1]
                    battery_2 = batteries[index_b2]

                # Select house
                index_h = random.randint(len(connections[battery_1]))
                output_h = connections[battery_1][index_h].capacity

                # Battery 1 decreases and battery 2 increases
                if abs((occupied_c[index_b1] - output_h) - capacities[index_b1]) < abs((occupied_c[index_b1]) - capacities[index_b1]):
                        if abs((occupied_c[index_b2] + output_h) - capacities[index_b2]) < abs((occupied_c[index_b2]) - capacities[index_b2]):
                            break
            
            # Switch the house (Delete from battery 1 and add to battery 2)
            connections[battery_2].append(connections[battery_1][index_h])
            connections[battery_1].pop(index_h)
            
            # Update capacity 
            occupied_c[index_b1] -= output_h
            occupied_c[index_b2] += output_h
            battery_1.occupied_capacity -= output_h
            battery_2.occupied_capacity += output_h           

        # Switch two houses
        else:
            while True:
                tries += 1
                print(tries)
                # Select batteries
                battery_1, battery_2 = 0, 0
                while battery_1 == battery_2:
                    index_b1 = random.choice([0, 1, 2, 3, 4])
                    index_b2 = random.choice([0, 1, 2, 3, 4])
                    battery_1 = batteries[index_b1]
                    battery_2 = batteries[index_b2]

                # Select houses
                index_h1 = random.randint(len(connections[battery_1]))
                index_h2 = random.randint(len(connections[battery_2]))
                output_h1 = connections[battery_1][index_h1].capacity
                output_h2 = connections[battery_2][index_h2].capacity

                diff = output_h1 - output_h2

                if output_h1 > output_h2: #B1 decreases and B2 increases
                    if abs((occupied_c[index_b1] - diff) - capacities[index_b1]) < abs((occupied_c[index_b1]) - capacities[index_b1]):
                        if abs((occupied_c[index_b2] + diff) - capacities[index_b2]) < abs((occupied_c[index_b2]) - capacities[index_b2]):
                            break

                else:             #B1 increases and B2 decreases
                    if abs((occupied_c[index_b1] - diff) - capacities[index_b1]) < abs((occupied_c[index_b1]) - capacities[index_b1]):
                        if abs((occupied_c[index_b2] + diff) - capacities[index_b2]) < abs((occupied_c[index_b2]) - capacities[index_b2]):
                            break

            # Switch the houses
            house1 = connections[battery_1][index_h1]
            connections[battery_1][index_h1] = connections[battery_2][index_h2]
            connections[battery_2][index_h2] = house1

            # Update capacities
            occupied_c[index_b1] -= diff
            occupied_c[index_b2] += diff
            battery_1.occupied_capacity -= diff
            battery_2.occupied_capacity += diff

    return connections

if __name__ == "__main__":
    s = Smartgrid("1")
    b, h = s.get_data()
    connections = random_state_generator(b, h)

    new_connections = make_solution(b, connections)
    
