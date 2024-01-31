from main import Smartgrid
from numpy import random


def heuraka(occupied_c, capacities):
    """Checks if the batteries capacities aren't exceeded
    Pre:
        occupied_c (list[float]): List of the occupied capacity of the batteries
        capacities (list[int]): List of the capacity of the batteries.

    Post:
        bool: True when all the occupied capacities are below the capacity.
    """    
    for i in range(len(capacities)):
        if occupied_c[i] > capacities[i]:
            return False
    return True


def make_solution(b, state):
    """Converts a random distrubution of houses into a solution,
    where the batteries capcities aren't exceeded.

    Pre:
        b (dict[int: object]): List of the battery objects
        state (dict[object: list[object]]): The distribution of houses over the batteries


    Post:
        state (dict[object: list[object]]): A solution where the constraint is met
    """    

    # Make lists that are needed to check the constraint
    occupied_c = []
    capacities = []
    for key, battery in b.items():
        occupied_c.append(battery.occupied_capacity)
        capacities.append(battery.capacity)

    # make a copy of the state and occupied capacities
    copy_dict = state.copy()
    copy_c = occupied_c.copy()

    # Make a solution by switching 1 or 2 house(s) repeatedly
    j = 0
    tries = 0

    # Loop till a solution is found or 
    # if there is a very small chance left of finding a solution (j > 6000)
    while not heuraka(occupied_c, capacities):
        j += 1

        # Generate random integer to decide if one or two houses need to be changed
        p = random.uniform(0, 1)
        
        # Switch one house
        if p < 0.15:
            while True:
                tries += 1
                
                # Dont switch one house anymore when 1000 interations have been executed
                if tries > 1000:
                    break

                # Select random battery
                battery_1, battery_2 = 0, 0
                while battery_1 == battery_2:
                    index_b1 = random.choice([0, 1, 2, 3, 4])
                    index_b2 = random.choice([0, 1, 2, 3, 4])
                    battery_1 = b[index_b1]
                    battery_2 = b[index_b2]

                # Select random house
                index_h = random.randint(0, len(state[battery_1]) - 1)
                output_h = state[battery_1][index_h].capacity

                # Check if the difference between the occupied capacity and the capacity of the battery decreases
                if abs((occupied_c[index_b1] - output_h) - capacities[index_b1]) < abs((occupied_c[index_b1]) - capacities[index_b1]):
                        if abs((occupied_c[index_b2] + output_h) - capacities[index_b2]) < abs((occupied_c[index_b2]) - capacities[index_b2]):
                            break

                # Stop trying to find a solution when 6000 interations have been reached
                if tries > 6000:
                    return 1
                

            # Switch the house            
            if tries < 1000:
                state[battery_2].append(state[battery_1].pop(index_h))
            
                # Update capacity 
                occupied_c[index_b1] -= output_h
                occupied_c[index_b2] += output_h
                battery_1.occupied_capacity -= output_h
                battery_2.occupied_capacity += output_h           

        # Switch two houses
        else:
            while True:
                tries += 1

                # Select two random batteries
                battery_1, battery_2 = 0, 0
                while battery_1 == battery_2:
                    index_b1 = random.choice([0, 1, 2, 3, 4])
                    index_b2 = random.choice([0, 1, 2, 3, 4])
                    battery_1 = b[index_b1]
                    battery_2 = b[index_b2]

                # Select two random houses
                index_h1 = random.randint(len(state[battery_1]))
                index_h2 = random.randint(len(state[battery_2]))
                output_h1 = state[battery_1][index_h1].capacity
                output_h2 = state[battery_2][index_h2].capacity

                diff = output_h1 - output_h2

                # Check if the difference between the occupied capacity and the capacity of the battery decreases
                # Battery1 decreases and battery 2 increases
                if output_h1 > output_h2:
                    if abs((occupied_c[index_b1] - diff) - capacities[index_b1]) < abs((occupied_c[index_b1]) - capacities[index_b1]):
                        if abs((occupied_c[index_b2] + diff) - capacities[index_b2]) < abs((occupied_c[index_b2]) - capacities[index_b2]):
                            break

                # Battery 1 increases and battery 2 decreases
                else:             
                    if abs((occupied_c[index_b1] - diff) - capacities[index_b1]) < abs((occupied_c[index_b1]) - capacities[index_b1]):
                        if abs((occupied_c[index_b2] + diff) - capacities[index_b2]) < abs((occupied_c[index_b2]) - capacities[index_b2]):
                            break

                # Stop trying to find a solution when 6000 interations have been reached
                if tries > 6000:
                    return 1

            # Switch the houses
            house1 = state[battery_1][index_h1]
            state[battery_1][index_h1] = state[battery_2][index_h2]
            state[battery_2][index_h2] = house1

            # Update capacities
            occupied_c[index_b1] -= diff
            occupied_c[index_b2] += diff
            battery_1.occupied_capacity -= diff
            battery_2.occupied_capacity += diff

    return state



    
