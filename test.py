from itertools import permutations

# Sample dictionary with keys and lists
data = {
    'key1': [1, 2, 3],
    'key2': ['a', 'b', 'c'],
    'key3': ['x', 'y', 'z']
}

# Generate permutations of values (lists)
values_permutations = permutations(data.values())

# Iterate through permutations
for values_permutation in values_permutations:
    # Create a new dictionary for the current permutation
    new_dict = {}
    for key, value in zip(data.keys(), values_permutation):
        new_dict[key] = value
    print(new_dict)