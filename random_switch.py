from numpy import random

def random_switch(batteries, connections):
    
    battery_1, battery_2 = 0, 0
    while battery_1 == battery_2:
        battery_1 = batteries[random.choice([0, 1, 2, 3, 4])]
        battery_2 = batteries[random.choice([0, 1, 2, 3, 4])]

    while True:
        index_1 = random.randint(len(connections[battery_1]))
        index_2 = random.randint(len(connections[battery_2]))

        cap_1 = connections[battery_1][index_1].capacity
        cap_2 = connections[battery_2][index_2].capacity

        diff = abs(cap_1 - cap_2)

        if cap_1 > cap_2:
            if battery_1.occupied_capacity + diff < 1506:
                break

        else:
            if battery_2.occupied_capacity + diff < 1506:
                break

    # Switch the houses
    house1 = connections[battery_1][index_1]
    connections[battery_1][index_1] = connections[battery_2][index_2]
    connections[battery_2][index_2] = house1

    if cap_1 > cap_2:
        battery_1.occupied_capacity += diff
        battery_2.occupied_capacity -= diff

    else:
        battery_1.occupied_capacity -= diff
        battery_2.occupied_capacity += diff

    return connections

        


