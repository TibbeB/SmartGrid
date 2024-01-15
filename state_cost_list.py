N = 0
states_costs_list = {}

# create N random states
for i in range(N):

    district = "1"
    
    # create SmartGrid instance
    smartgrid = Smartgrid(district)
    
    # return battery and house objects
    batteries, houses = smartgrid.get_data()
    
    # generate random state
    state = smartgrid.tibbe_function(batteries, houses)
    
    # calculate costs of state
    cost = smartgrid.cost_shared(state)
    
    # checks if state doesn't alreday exist
    if state not in states_costs_list:
    
        # append state and costs to dict
        states_cost_list[state] = cost

# determine minimum cost in statespace
minimum = min(states_cost_shared.values())

minimum_list = []

# find states with minimun costs
for s in states_cost_shared:
    c = states_cost_shared[s]
    if c == minimum:
        minimum_list.append(s)
    
    
    