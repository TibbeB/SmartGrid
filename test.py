import numpy as np

occupied_c = np.array([2, 4, 6])
capacities = np.array([3, 3, 8])

if np.all(occupied_c < capacities):
    print("True")
else:
    print("False")