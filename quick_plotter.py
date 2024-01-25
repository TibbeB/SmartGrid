import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter
import matplotlib
import numpy as np
matplotlib.use('TkAgg')

def quick_plot(connections, cables):
    
    colors = ['brown','yellow','lime','crimson','cyan']
    
    color_counter = 0
    
    battery_img = mpimg.imread('accu.jpg')
    
    house_img = mpimg.imread('house.jpg')
    
    fig, ax = plt.subplots()
    
    for battery, houses in connections.items():
        
        ax.imshow(battery_img, extent=(battery.x-2, battery.x+2, battery.y-2, battery.y+2))
        
        for house in houses:
            
            ax.imshow(house_img, extent=(house.x-1, house.x+1, house.y-1, house.y+1))
            
            cable = cables[house.identification]
            
            cable_length = len(cable.path)
            x = []
            y = []
            
            for i in range(cable_length):
                x.append(cable.path[i][0])
                y.append(cable.path[i][1])
            
            ax.plot(x,y, color = colors[color_counter])
             
        color_counter += 1
       
    ax.set_aspect('equal', adjustable='box')

    plt.show()