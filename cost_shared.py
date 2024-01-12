def cost_shared(self, dictionary, cable_dict):
    total_cost = 0
    for battery, houses in dictionary:
        total_cost += 5000
        for house in houses:
            total_cost += 9 * (len(cable_dict[house.identification].path) - 1)
        
    return total_cost