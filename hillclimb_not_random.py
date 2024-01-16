from FFD import even_distribution
from x_y_path import x_y_path
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


def hillclimb_random(smartgrid, batteries, houses, N):
    costs_all = []
    costs_low = []
    itterations = []

    # generate starting state
    distribution = even_distribution(batteries, houses)
    smartgrid.x_y_path(distribution)

    # calculating the total cost
    costs = smartgrid.cost_shared(distribution)
    costs_low.append(costs)

    # make random steps from the starting state
    for i in range(N):
        for key, cable in smartgrid.cables.items():
            cable.clear_cable()
        
        state = random_switch(batteries, distribution)
        smartgrid.x_y_path(distribution)

        new_cost = smartgrid.cost_shared(state)
        costs_all.append(new_cost)
        itterations.append(i)

        if new_cost < costs:
            
            costs = new_cost
            distribution = state
            costs_low.append(costs)

    return distribution, costs_low
