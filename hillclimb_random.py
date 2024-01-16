from FFD import even_distribution
from random_switch import random_switch

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
