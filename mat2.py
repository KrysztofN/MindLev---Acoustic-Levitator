import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

def particle_walk(x, y, z, radius, axis):
    steps = 1000
    step_size = 0.1
    walk = np.zeros((steps, 3))
    angle = np.linspace(0, 2 * np.pi, steps)
    
    if axis == 'horizontal':
        walk[:,0] = x + radius * np.cos(angle)
        walk[:,1] = y + radius * np.sin(angle)
        walk[:,2] = z + step_size * np.arange(steps)
    elif axis == 'vertical':
        walk[:,0] = x + step_size * np.arange(steps)
        walk[:,1] = y + radius * np.cos(angle)
        walk[:,2] = z + radius * np.sin(angle)
    else:
        raise ValueError('Invalid axis input')
        
    return walk

def plot_walk():
    x = float(x_entry.get())
    y = float(y_entry.get())
    z = float(z_entry.get())
    radius = float(radius_entry.get())
    axis = axis_var.get()
    num_paths = int(num_paths_entry.get())
    
    start = [x, y, z]
    walk = np.zeros((0, 3))
    
    for i in range(num_paths):
        walk = np.concatenate((walk, particle_walk(*start, radius, axis)))
        start[2] = walk[-1, 2]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(walk[:,0], walk[:,1], walk[:,2])
    plt.show()

root = tk.Tk()
root.title("3D Particle Walk")

frame = tk.Frame(root)
frame.pack()

x_label = tk.Label(frame, text="X:")
x_label.grid(row=0, column=0, sticky="W")
x_entry = tk.Entry(frame)
x_entry.grid(row=0, column=1)

y_label = tk.Label(frame, text="Y:")
y_label.grid(row=1, column=0, sticky="W")
y_entry = tk.Entry(frame)
y_entry.grid(row=1, column=1)

z_label = tk.Label(frame, text="Z:")
z_label.grid(row=2, column=0, sticky="W")
z_entry = tk.Entry(frame)
z_entry.grid(row=2, column=1)

radius_label = tk.Label(frame, text="Radius:")
radius_label.grid(row=3, column=0, sticky="W")
radius_entry = tk.Entry(frame)
radius_entry.grid(row=3, column=1)

num_paths_label = tk.Label(frame, text="Number of Paths:")
num_paths_label.grid(row=4, column=0, sticky="W")
num_paths_entry = tk.Entry(frame)
num_paths_entry.grid(row=4, column=1)

axis_label = tk.Label(frame, text="Axis:")
axis_label.grid(row=5, column=0, sticky="W")
axis_var = tk.StringVar()
horizontal_radio = tk.Radiobutton(frame, text="Horizontal", variable=axis_var, value="horizontal")
horizontal_radio.grid(row=5, column=1, sticky="W")
vertical_radio = tk.Radiobutton(frame, text="Vertical", variable=axis_var, value="vertical")
vertical_radio.grid(row=5, column=1)

plot_button = tk.Button(frame, text="Animate", command=plot_walk)
plot_button.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()

