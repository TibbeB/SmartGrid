import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter
import matplotlib
import numpy as np
matplotlib.use('TkAgg')

def quick_plot(connections: dict[object, list[object]], cables: dict[int, object]) -> None:
    """
    creates visual representation of state
    
    pre:
    - connections (dict[object, list[object]]): state represented in dict
    - cables (dict[int, object]): cables dict
    post:
    - visualizes state by creating a plot
    """
    
    # paths specific to batteries colors
    colors = ['black','yellow','lime','crimson','cyan']
    
    color_counter = 0
    
    # battery img
    battery_img = mpimg.imread('accu.jpg')
    
    # house img
    house_img = mpimg.imread('house.jpg')
    
    fig, ax = plt.subplots()
    
    for battery, houses in connections.items():
        
        # add battery img
        ax.imshow(battery_img, extent=(battery.x-2, battery.x+2, battery.y-2, battery.y+2))
        
        for house in houses:
            
            # add house img
            ax.imshow(house_img, extent=(house.x-1, house.x+1, house.y-1, house.y+1))
            
            cable = cables[house.identification]
            
            cable_length = len(cable.path)
            x = []
            y = []
            
            # lay cables
            for i in range(cable_length):
                x.append(cable.path[i][0])
                y.append(cable.path[i][1])
            
            ax.plot(x,y, color = colors[color_counter], linewidth = 2.5)
             
        color_counter += 1
       
    ax.set_aspect('equal', adjustable='box')

    plt.show()