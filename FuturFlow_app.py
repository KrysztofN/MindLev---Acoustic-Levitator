from tkinter import ttk
from tkinter import *
from customtkinter import *
import math
from PIL import ImageTk, Image
import threading
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
import numpy as np
from tkinter import font
import time
import tkinter.colorchooser as colorchooser
from mat import *
from mat1 import *
import struct
import serial
import time
from ok import *







#---------------------------------------------------Initialize the particle-------------------------------------------------------------------
# this code starts when an app is opened. It initializes the particle to always start at fixed coordinates 

global initialized
initialized = False

def initialize_s():
    ser = serial.Serial(port='COM5', baudrate=921600)

    global initialized
    initialized = True

    start = np.array((72, 72, 0))
    end =  np.array((72, 72, 100))

    # Calculate the direction vector and distance between the start and end points

    distance = np.linalg.norm(end - start)
    direction = (end - start) / distance

    # Generate the steps of the walk with a step size of 0.1
    steps = np.arange(0, distance + 1, 1)

    print("Steps of the walk:")
    for step in steps:
        x,y,z = np.round(start + direction * step, 2)
        #calculate_phases(x,y,z)
        print(x,y,z)
        calculate_phases__ini(x,y,z)

    i = 0
    data = b''
    for i ,phase in enumerate(phases_ini):
        data += struct.pack('>BB', i % 200, int(phase))
    ser.write(data)

    
    phases_ini.clear()
    ser.close()
    



# main window
window = CTk()
window.title("FuturFlow Simulator")
window.configure(fg_color='#2d2d30')

# user-dynamic adjustable window
window.state('zoomed')
window.option_add("*Font","Verdana 10")

style = ttk.Style()
style.configure("TNotebook.Tab", font=("",10))



# -----------------------------------------Section one-----------------------------------------------------


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import win32gui
import win32con
import tkinter as tk
import os


#set the pygame window coordinates
x = 0
y = 55
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

# Define the boundaries of the sphere

MIN_X, MAX_X = -100.0, 100.0
MIN_Y, MAX_Y = -100.0, 100.0
MIN_Z, MAX_Z = -100.0, 0.0

#Initialize pygame
pygame.init()
clock = pygame.time.Clock()


def on_close():
    pygame.quit()
    sys.exit()

for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on_close()


def gett():
    global step_entry, step
    step = float(step_entry.get())

# commands
def move_left():
    gett()
    global sphere_x
    if sphere_x - step >= MIN_X:
        sphere_x -= step

def move_right():
    gett()
    global sphere_x
    if sphere_x + step <= MAX_X:
        sphere_x += step

def move_up():
    gett()
    global sphere_y
    if sphere_y + step <= MAX_Y:
        sphere_y += step

def move_down():
    gett()
    global sphere_y
    if sphere_y - step >= MIN_Y:
        sphere_y -= step

def move_backward():
    gett()
    global sphere_z
    if sphere_z - step >= MIN_Z:
        sphere_z -= step

def move_forward():
    gett()
    global sphere_z
    if sphere_z + step <= MAX_Z:
        sphere_z += step


def sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricDrawStyle(quad, GLU_FILL)
    gluSphere(quad, radius, slices, stacks)
    

    

    selected_color = app.get_selected_color()
        # Convert the color to the format used by Pygame
    if  selected_color is not None:
        rgb_color = hex_to_rgb(selected_color)
        pygame_color = (rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)

        # Set the color for Pygame
        glColor(*pygame_color)
    #else:
        #print("No color selected")

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb




def move_sphere():
    global sphere_x, sphere_y, sphere_z
    glTranslatef(sphere_x,sphere_y,sphere_z)
    
def rotate_view(angle, axis):
    glRotatef(angle, *axis)

def create_pygame_window():
    global screen
    #flags = pygame.NOFRAME
    #pygame.display.set_mode((display), flags, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("3D Simulation")
    display_flags = pygame.DOUBLEBUF | pygame.OPENGL #| NOFRAME
    display = (1565, 975)
    screen = pygame.display.set_mode(display, display_flags)
    
    #pygame.display.set_mode((600,600), DOUBLEBUF|OPENGL, pygame.NOFRAME)
    hwnd = pygame.display.get_wm_info()['window']
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)



    global sphere_x, sphere_y, sphere_z
    sphere_x, sphere_y, sphere_z = 0.0, 0.0, 0.0

    gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -12)

    
    global step_entry
    global sphere_radius
    sphere_radius = 0.1
    
    i = 0 
    while True:
        for event in pygame.event.get():

            
            if event.type == pygame.QUIT:
               on_close()
                
                

                    # Get the sphere radius from the tkinter entry
            try:
                sphere_radius = float(radius_s_entry.get())
            except ValueError:
                pass

        window.update()



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_left()
        if keys[pygame.K_RIGHT]:
            move_right()
        if keys[pygame.K_UP]:
            move_up()
        if keys[pygame.K_DOWN]:
            move_down()
        if keys[pygame.K_z]:
            move_backward()
        if keys[pygame.K_x]:
            move_forward()

        #move_sphere()
        #sphere_x, sphere_y, sphere_z = positions[i]
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(sphere_x, sphere_y, sphere_z)
        

        # Rotate the view
        rotate_view(angle=1, axis=(1, 0, 0))

        sphere(sphere_radius, 20, 20)
        glPopMatrix()

        '''i += 1
        if i >= len(positions):
            i = 0'''
        
        pygame.display.flip()
        pygame.time.wait(10)
        clock.tick(60)
        


        

def show_pygame_window():
    create_pygame_window()

def main():
    if (step_entry.get()==""):
        messagebox.showerror('Value error', 'Insert correct initial vlues x,y,z, and step size')
    else:
        start_pygame()
        
    
    
def start_pygame():
    # Start a new thread for the Pygame event loop
    threading.Thread(target=show_pygame_window).start()
    





#-------------------------------------------------------------END--------------------------------------------------------------------







#------------------------------------------------------------MENU------------------------------------------------------------------

# MENUBAR

#Menubar

def exit_on():
    window.quit()

menubar = Menu(window)
window.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "Save")
fileMenu.add_command(label = "Open")
fileMenu.add_command(label = "None")
fileMenu.add_command(label = "None")
fileMenu.add_command(label = "None")
fileMenu.add_command(label = "None")
fileMenu.add_command(label = "None")
fileMenu.add_command(label = "None")
fileMenu.add_command(label = "Exit", command = exit_on)



# Editmenu

def openFile():
    print("File has been opened")

def saveFile():
    print("File has been saved!")

def save_as_File():
    print("File has been saved!")

def cut():
    print("File has been cut")

# Opening and resizing Images

openImage = Image.open('zdjęcia/ph3.png')
saveImage = Image.open('zdjęcia/ph1.png')
cutImage = Image.open('zdjęcia/ph6.png')
save_asImage = Image.open('zdjęcia/ph5.png')
graphImage = Image.open('zdjęcia/ph4.png')

openRImage = ImageTk.PhotoImage(openImage.resize((13,13), Image.ANTIALIAS))
saveRImage = ImageTk.PhotoImage(saveImage.resize((13,13), Image.ANTIALIAS))
cutRImage = ImageTk.PhotoImage(cutImage.resize((13,13), Image.ANTIALIAS))
save_asRImage = ImageTk.PhotoImage(save_asImage.resize((13,13), Image.ANTIALIAS))
graphRImage = ImageTk.PhotoImage(graphImage.resize((13,13), Image.ANTIALIAS))

editMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Edit", menu = editMenu)
editMenu.add_command(label = "Open", command = openFile, image = openRImage, compound = "left" )
editMenu.add_command(label = "Cut", command = cut, image = cutRImage, compound = "left")
editMenu.add_command(label = "Save", command = saveFile, image = saveRImage, compound = "left")
editMenu.add_command(label = "Save as", command = save_as_File, image = save_asRImage, compound = "left")


# simulation menu

def simulation_win():
    simwin = CTkToplevel(window)
    simwin.title("SImulation parameters")
    simwin.resizable(False,False)
    simwin.geometry("+100+100")
    simwin.lift()
    simwin.attributes("-topmost", True)

    l1 = CTkLabel(simwin, text = "Particle speed:")
    l1.grid(row=0, column = 0, pady = 5, padx = 5)
    l1_entry = CTkEntry(simwin)
    l1_entry.grid(row=0, column = 1, pady = 5, padx = 5)

    l2 = CTkLabel(simwin, text = "Particle radius:")
    l2.grid(row=1, column = 0, pady = 5, padx = 5)
    l2_entry = CTkEntry(simwin)
    l2_entry.grid(row=1, column = 1, pady = 5, padx = 5)


    l3 = CTkLabel(simwin, text = "Medium speed:")
    l3.grid(row=2, column = 0, pady = 5, padx = 5)
    l3_entry = CTkEntry(simwin)
    l3_entry.grid(row=2, column = 1, pady = 5, padx = 5)

    l4 = CTkLabel(simwin, text = "Medium density:")
    l4.grid(row=3, column = 0, pady = 5, padx = 5)
    l4_entry = CTkEntry(simwin)
    l4_entry.grid(row=3, column = 1, pady = 5, padx = 5)

    #Menu Medium
    mediummenu_var = StringVar(value="Air")  # set initial value

    def optionmenu_callback_1(choice):
        print("optionmenu dropdown clicked:", choice)

    mediumbox = CTkOptionMenu(simwin,
                                        values=["Air"],
                                        command=optionmenu_callback_1,
                                        variable=mediummenu_var)
    mediumbox.grid(row=4, column = 0,padx=20, pady=10)

    #Menu particle material
    materialmenu_var = StringVar(value="Expanded Polysteryne(EPS)")  # set initial value

    def optionmenu_callback_2(choice):
        print("optionmenu dropdown clicked:", choice)

    particlebox = CTkOptionMenu(simwin,
                                        values=["Expanded Polysteryne(EPS)"],
                                        command=optionmenu_callback_2,
                                        variable=materialmenu_var)
    particlebox.grid(row=4, column = 1,padx=20, pady=10)


Simulationmenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Simulation", menu = Simulationmenu)
Simulationmenu.add_command(label = "RUN" ,command = main) #pygame_opened()))
Simulationmenu.add_command(label = "Edit parameters", command = simulation_win)






# Transducermenu

def assignment():
    
    def display_bottom():
        # Clear the canvas
        canvas.delete("all")

        canvas.config(width=cols * 60, height=rows * 60)

        for i, row in enumerate(bottom):
            for j, val in enumerate(row):
                canvas.create_text(j * 60 + 20, i * 60 + 20, text=str(val), fill = "White", font=(13))

   
    def display_top():
        
        canvas.delete("all")

        canvas.config(width=cols * 60, height=rows * 60)

        # Display the top array
        for i, row in enumerate(top):
            for j, val in enumerate(row):
                canvas.create_text(j * 60 + 20, i * 60 + 20, text=str(val), fill = "White", font=(13))

    root = CTkToplevel()
    root.config(bg= "#1a1a1a")
    root.resizable(FALSE,FALSE)

    rows = 10
    cols = 10

    # Create the bottom and top arrays
    bottom = [[j + 1 + i * cols for j in range(cols)] for i in range(rows)]
    top = [[j + 1 + i * cols + rows * cols for j in range(cols)] for i in range(rows)]

    canvas = tk.Canvas(root, width=cols * 60, height=rows * 60, background="#1a1a1a", highlightbackground="#387bc8", highlightthickness=2)
    canvas.pack(side="bottom")

    button_frame = CTkFrame(root)
    button_frame.pack(side="left")
    button_frame.configure(fg_color='#000000', bg_color = '#000000' )

    bottom_button = CTkButton(button_frame, text="Bottom Array", command=display_bottom)
    bottom_button.grid(row = 0, column = 0, pady = 20, padx = 51)

    top_button = CTkButton(button_frame, text="Top Array", command=display_top)
    top_button.grid(row = 0, column = 1, pady = 20, padx = 51)



trmenu =  Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Transducers", menu = trmenu)
trmenu.add_command(label = "Assignment", command = assignment)
trmenu.add_command(label = "Calculate")
trmenu.add_command(label = "Alternate")

# Chartmenu
Chartmenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Charts", menu = Chartmenu)
Chartmenu.add_command(label = "Create", image = graphRImage, compound = "left")
Chartmenu.add_command(label = "Export to excel")
Chartmenu.add_command(label = "Assignment")
Chartmenu.add_command(label = "Assignment")


# Variousmenu
Variousmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Various", menu = Variousmenu)
Variousmenu.add_command(label = "Assignment")
Variousmenu.add_command(label = "Assignment")
Variousmenu.add_command(label = "Assignment")
Variousmenu.add_command(label = "Assignment")
Variousmenu.add_command(label = "Assignment")


#---------------------------------------------------------------MENU END------------------------------------------------------------------




#--------------------------------------------------------------Draw section----------------------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button

def draw_plot():
    global initialized
  
    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
    

        fig, ax = plt.subplots()
        ax.set_xlim([0, 160])
        ax.set_ylim([0, 160])
        

        x_mesh, y_mesh = np.meshgrid(np.arange(0, 161, 1), np.arange(0, 161, 1))
        mesh_points = np.column_stack((x_mesh.ravel(), y_mesh.ravel()))

        

        ax.scatter(mesh_points[:, 0], mesh_points[:, 1], s=1, color='violet')

        line = Line2D([], [], color='red')
        ax.add_line(line)

        xdata = []
        ydata = []

        def find_closest_point(point, mesh_points):
            distances = np.linalg.norm(mesh_points - point, axis=1)
            closest_index = np.argmin(distances)
            closest_point = mesh_points[closest_index]
            return closest_point

        def on_press(event):
            global xdata, ydata
            xdata = [event.xdata]
            ydata = [event.ydata]
            line.set_data(xdata, ydata)
        
        def send_uart():
            ser = serial.Serial(port='COM5', baudrate=921600)
            data = b''
            
            for i, phase in enumerate(phases_ini):
                data += struct.pack('>BB', i % 200, int(phase))

            for i, phase in enumerate(phases_new):
                data += struct.pack('>BB', (i+len(phases_ini)) % 200, int(phase))

            ser.write(data)
            #print("Sent data over serial port: ", data)
            phases_ini.clear()
            phases_new.clear()
            ser.close()

            #print(phases_new)
            phases_new.clear()
            phases_ini.clear()
            ser.close()

        def send_uart_v2():
            ser = serial.Serial(port='COM5', baudrate=921600)
            data = b''
            
            for i, phase in enumerate(phases_ini):
                data += struct.pack('>BB', i % 200, int(phase))
            
            ser.write(data)
            #print("Sent data over serial port: ", data)
            phases_ini.clear()
            ser.close()

        def on_release(event):
            global xdata, ydata
            xdata.append(event.xdata)
            ydata.append(event.ydata)

            #--------------------------------------------------------------------------------------------------------------------
            start = np.array((72, 72, 100))  
            end =  np.array((xdata[0], ydata[0], 72))

            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            steps = np.arange(0, distance + 0.5, 0.5)
            phases_new.clear()
            phases_ini.clear()

            print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                print(x,y,z)
                calculate_phases__ini(x,y,z)


            #----------------END INITIALIZATION-----------------------------------------------------------------------------------


          
            path_points = np.column_stack((xdata, ydata))
            closest_points = [find_closest_point(point, mesh_points) for point in path_points]

          
            interpolated_points = []
            for i in range(len(closest_points) - 1):
                start = closest_points[i]
                end = closest_points[i + 1]
                delta = end - start
                distance = np.linalg.norm(delta)
                num_steps = int(distance / 0.5)
                if num_steps == 0:
                    interpolated_points.append(start)
                else:
                    step_size = delta / num_steps
                    for j in range(num_steps + 1):
                        point = start + j * step_size
                        interpolated_points.append(point)

           
            for point in interpolated_points:
                #print("Interpolated point on mesh: ({:.2f}, {:.2f}, {:.2f})".format(point[0], point[1], 72))
                calculate_phases_new(int(point[0]),int(point[1]), 72)

            '''print("phases_ini")
            print(len(phases_ini))
            print("phases_new")
            print(len(phases_new))'''
            send_uart()
            

            start = np.array((point[0], point[1],72)) 
            end =  np.array((72,72,100))

            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            steps = np.arange(0, distance + 0.4, 0.4)
            phases_new.clear()
            phases_ini.clear()

            #print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                #print(x,y,z)
                calculate_phases__ini(x,y,z)
            
            send_uart_v2()


            x_interp = [point[0] for point in interpolated_points]
            y_interp = [point[1] for point in interpolated_points]
            line.set_data(x_interp, y_interp)
            fig.canvas.draw_idle()

        def on_motion(event):
            global xdata, ydata
            if event.button == 1:
                xdata.append(event.xdata)
                ydata.append(event.ydata)
                line.set_data(xdata, ydata)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('button_release_event', on_release)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        
    
        plt.xlabel("X coordinates", fontdict = {"fontsize":10})
        plt.ylabel("Y coordinates", fontdict = {"fontsize":10})
        plt.title("PATH DRAWER", fontdict = {"fontsize":20})
        

        plt.show()




#-------------------------------------------------------------------------Draw vertically---------------------------------------------------------



def draw_plot_v2():
    global initialized

    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
    

        fig, ax = plt.subplots()
        ax.set_xlim([0, 160])
        ax.set_ylim([0, 200])
        

    
        x_mesh, y_mesh = np.meshgrid(np.arange(0, 160.2, 0.2), np.arange(0, 200.2, 0.2))
        mesh_points = np.column_stack((x_mesh.ravel(), y_mesh.ravel()))

        

        ax.scatter(mesh_points[:, 0], mesh_points[:, 1], s=1, color='green')

        line = Line2D([], [], color='red')
        ax.add_line(line)

        xdata = []
        ydata = []

        def find_closest_point(point, mesh_points):
            # Find the closest point on the mesh to the given point
            distances = np.linalg.norm(mesh_points - point, axis=1)
            closest_index = np.argmin(distances)
            closest_point = mesh_points[closest_index]
            return closest_point

        def on_press(event):
            global xdata, ydata
            xdata = [event.xdata]
            ydata = [event.ydata]
            line.set_data(xdata, ydata)
        
        def send_uart():
            ser = serial.Serial(port='COM5', baudrate=921600)
            data = b''
            
            for i, phase in enumerate(phases_ini):
                data += struct.pack('>BB', i % 200, int(phase))

            for i, phase in enumerate(phases_new):
                data += struct.pack('>BB', (i+len(phases_ini)) % 200, int(phase))

            ser.write(data)
            #print("Sent data over serial port: ", data)
            phases_ini.clear()
            phases_new.clear()
            ser.close()

            #print(phases_new)
            phases_new.clear()
            phases_ini.clear()
            ser.close()
        
        def send_uart_2():
            ser = serial.Serial(port='COM5', baudrate=921600)
            data = b''
            
            for i, phase in enumerate(phases_ini):
                data += struct.pack('>BB', i % 200, int(phase))
            
            ser.write(data)
            #print("Sent data over serial port: ", data)
            phases_ini.clear()
            ser.close()


        def on_release(event):
            global xdata, ydata
            xdata.append(event.xdata)
            ydata.append(event.ydata)

            #--------------------------------------------------------------------------------------------------------------------
            start = np.array((72, 72, 100))  
            end =  np.array((xdata[0], 72, ydata[0]))

            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            steps = np.arange(0, distance + 0.5, 0.5)
            phases_new.clear()
            phases_ini.clear()

            #print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                #print(x,y,z)
                calculate_phases__ini(x,y,z)


            #----------------END INITIALIZATION-----------------------------------------------------------------------------------


            # Find the closest point on the mesh to each point on the path
            path_points = np.column_stack((xdata, ydata))
            closest_points = [find_closest_point(point, mesh_points) for point in path_points]

            # Perform linear interpolation between the closest points on the mesh
            interpolated_points = []
            for i in range(len(closest_points) - 1):
                start = closest_points[i]
                end = closest_points[i + 1]
                delta = end - start
                distance = np.linalg.norm(delta)
                num_steps = int(distance / 0.05)
                if num_steps == 0:
                    interpolated_points.append(start)
                else:
                    step_size = delta / num_steps
                    for j in range(num_steps + 1):
                        point = start + j * step_size
                        interpolated_points.append(point)

            # Print the interpolated points
            for point in interpolated_points:
                #print("Interpolated point on mesh: ({:.2f}, {:.2f}, {:.2f})".format(point[0], 72, point[1]))
                calculate_phases_new(int(point[0]),72, int(point[1]))

            '''print("phases_ini")
            print(len(phases_ini))
            print("phases_new")
            print(len(phases_new))'''
            send_uart()


            start = np.array((point[0], 72, point[1])) 
            end =  np.array((72,72,100))

            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            steps = np.arange(0, distance + 0.4, 0.4)
            phases_new.clear()
            phases_ini.clear()

            #print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                #print(x,y,z)
                calculate_phases__ini(x,y,z)
            
            send_uart_2()
            

            # Update the line with the interpolated points
            x_interp = [point[0] for point in interpolated_points]
            y_interp = [point[1] for point in interpolated_points]
            line.set_data(x_interp, y_interp)
            fig.canvas.draw_idle()

        def on_motion(event):
            global xdata, ydata
            if event.button == 1:
                xdata.append(event.xdata)
                ydata.append(event.ydata)
                line.set_data(xdata, ydata)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('button_release_event', on_release)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        
    
        plt.xlabel("X coordinates", fontdict = {"fontsize":10})
        plt.ylabel("Z coordinates", fontdict = {"fontsize":10})
        plt.title("PATH DRAWER", fontdict = {"fontsize":20})
        

        plt.show()



# Drawmenu
drawmenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label = "Draw", menu = drawmenu)
drawmenu.add_command(label = "Draw plot", command=draw_plot)
drawmenu.add_command(label = "Draw plot v2", command=draw_plot_v2)

'''# Drawmenu
drawmenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label = "Draw", menu = drawmenu)
drawmenu.add_command(label = "Draw plot", command=draw_plot)
'''

# --------------------------------------------------------------------------END DRAW-----------------------------------------------------------------










# -------------------------------------------------------------------------Section two---------------------------------------------------------------------

# Tabs
from tkinter.ttk import Notebook, Style

style = Style()
style.theme_use('classic')
style.configure('TNotebook', background = "#989aa1",highlightbackground='#afbabe', tabmargins = [0, 0, 0, 0] )
style.configure('TNotebook.Tab', font=('Helvetica', 10))


notebook = ttk.Notebook(window, style = "TNotebook")
tab1 = CTkFrame(notebook)
tab2 = CTkFrame(notebook)
tab3 = CTkFrame(notebook)
tab4 = CTkFrame(notebook)
tab5 = CTkFrame(notebook)


notebook.add(tab1, text = 'Main')
notebook.add(tab2, text = "M-Paths")
notebook.add(tab3, text ="Transdcures")
notebook.add(tab4, text = ' Traps ')
notebook.add(tab5, text = ' Points ')

notebook.pack(side=RIGHT)
notebook.config(width = 300, height = window.winfo_height())


# window button 1 activated
def open_new_window1():
    new_window_1 = Toplevel(window)
    new_window_1.title('1 button')


# window button 2 activated

def open_new_window2():
    new_window_2 = Toplevel(window)
    new_window_2.title('2 button')

# window button 3 activated

def open_new_window3():
    new_window_3 = Toplevel(window)
    new_window_3.title('3 button')

# window button 4 activated

def open_new_window4():
    new_window_4 = Toplevel(window)
    new_window_4.title('4 button')

# window button 5 activated
def open_new_window5():
    new_window_5 = Toplevel(window)
    new_window_5.title('5 button')

# window button 6 activated

def open_new_window6():
    new_window_6 = Toplevel(window)
    new_window_6.title('6 button')



# -----------------------------------------------------------Circular Path----------------------------------------------------------------------------



def open_new_window7():
    
    global initialized
    
    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    
    else:
    
        new_window_7 = CTkToplevel(window)
        new_window_7.title('Circular paths')
        new_window_7.resizable(False,False)
        new_window_7.geometry("+1040+100")

        

            
        stop_infinite = False
        stop_fixed = False

        def plot_walk(*args):
            run_walk()

            fig, ax = plt.subplots()
            circle = patches.Circle((x1, y1), radius, color='red', fill=False)
            ax.add_patch(circle)
            ax.set_xlim(x1-radius-1, x1+radius+1)
            ax.set_ylim(y1-radius-1, y1+radius+1)
            plt.show()


        def run_walk(*args):
            global x1
            global y1
            global z1
            global radius
            global axis_movement
            global user_choice
            global step_size

            x1 = int(entryx.get())
            y1 = int(entryy.get())
            z1 = int(entryz.get())
            radius = int(entry_radius.get())
            axis_movement = str(entry_axis.get())
            step_size = float(path_step.get())

            user_choice = path_entry.get()
            
            
            #---------------------------------------------------------------
            start = np.array((72, 72, 100)) 
            end =  np.array((x1, y1, z1))

            
            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            #step size = 0.1
            steps = np.arange(0, distance + 0.2, 0.2)

            
            #print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                #print(x,y,z)
                calculate_phases__ini(x,y,z)
            #print(phases_ini)


            #----------------END INITIALIZATION-------------------------------


            # Start the walk in a separate thread
            if user_choice == 'infinite':
                walk_thread = threading.Thread(target=start_infinite)
                walk_thread.start()
            elif user_choice.isdigit():
                user_choice = int(user_choice)
                walk_thread = threading.Thread(target=start_fixed, args=(user_choice,))
                walk_thread.start()
            else:
                raise ValueError("Invalid input. Enter 'infinite', a positive integer, or 'break'.")


        def start_infinite():
                    theta = 0

                    if axis_movement == "horizontal":
                        z = z1
                        while theta < 360:
                            x = x1 + radius * math.cos(math.radians(theta))
                            y = y1 + radius * math.sin(math.radians(theta))
                            calculate_phases_new(x-radius, y, z)
                            theta += step_size
                    elif axis_movement == "vertical_x":
                        x = x1
                        while theta < 360:
                            y = y1 + radius * math.cos(math.radians(theta))
                            z = z1 + radius * math.sin(math.radians(theta))
                            calculate_phases_new(x, y-radius, z)
                            theta += step_size
                    elif axis_movement == "vertical_y":
                        y = y1
                        while theta < 360:
                            x = x1 + radius * math.cos(math.radians(theta))
                            z = z1 + radius * math.sin(math.radians(theta))
                            calculate_phases_new(x-radius, y, z)
                            theta += step_size
                    else:
                        print("Invalid path type. Choose 'horizontal', 'vertical_x', or 'vertical_y'.")
                    theta = 0


        def start_fixed(user_choice):
                global stop_fixed
                stop_fixed = False
                theta = 0

                if stop_fixed:
                    pass
                else:
                    if axis_movement == "horizontal":
                        z = z1
                        while theta < 360:
                            x = x1 + radius * math.cos(math.radians(theta))
                            y = y1 + radius * math.sin(math.radians(theta))
                            calculate_phases_new(x-radius, y, z)
                            theta += step_size
                            if stop_fixed:
                                break
                    elif axis_movement == "vertical_x":
                        x = x1
                        while theta < 360:
                            y = y1 + radius * math.cos(math.radians(theta))
                            z = z1 + radius * math.sin(math.radians(theta))
                            calculate_phases_new(x, y-radius, z)
                            theta += step_size
                            if stop_fixed:
                                break
                    elif axis_movement == "vertical_y":
                        y = y1
                        while theta < 360:
                            x = x1 + radius * math.cos(math.radians(theta))
                            z = z1 + radius * math.sin(math.radians(theta))
                            calculate_phases_new(x-radius, y, z)
                            theta += step_size
                            if stop_fixed:
                                break
            

             #--------------------------------------------------------------------------------------------------------------------
                # problems with taking the last step 
                '''if axis_movement == "horizontal":
                    start = np.array((x-radius,y,z)) 
                elif axis_movement == "vertical_x":
                    start = np.array((x,y-radius,z))  
                elif axis_movement == "vertical_y":
                    start = np.array((x,y,z-radius))'''
                
                '''      start = np.array((x-radius,y,z)) 
                end =  np.array((80, 80, 50))

                # Calculate the direction vector and distance between the start and end points
                distance = np.linalg.norm(end - start)
                direction = (end - start) / distance

                # Generate the steps of the walk with a step size of 0.1
                steps = np.arange(0, distance + 0.1, 0.1)

                # Print the steps of the walk
                print("Steps of the walk:")
                for step in steps:
                    print(np.round(start + direction * step, 2))
                    get_speed()
                    time.sleep(speed_c)

                #----------------END INITIALIZATION-----------------------------------------------------------------------------------
                '''


        def calc_points_c():
            user_choice = path_entry.get()
            ser = serial.Serial(port='COM5', baudrate=921600, timeout = 60)


            if user_choice == "infinite":
                def infinite_loop_c():
        
                    i = 0
                    data = b''
                    for i ,phase in enumerate(phases_ini):
                        data += struct.pack('>BB', i % 200, int(round(phase)))
                    ser.write(data)
                    phases_ini.clear()

                    while True:
                        i = 0
                        data = b''
                        for i ,phase in enumerate(phases_new):
                            data += struct.pack('>BB', i % 200, int(round(phase)))
                        ser.write(data)


                        if stop_infinite:
                            break
                    phases_new.clear()
                    ser.close()

                thread = threading.Thread(target=infinite_loop_c)
                thread.start()
            else:
                def finite_loop_c():
                        
                        i = 0
                        if not phases_new:
                            print("None")
                        elif not phases_ini:
                            print("None")
                        else:
                            data = b''
                            for i, phase in enumerate(phases_ini):
                                data += struct.pack('>BB', i % 200, int(phase))
                            for i in range(int(user_choice)):
                                for i, phase in enumerate(phases_new):
                                    data += struct.pack('>BB', i % 200, int(phase))
                                ser.write(data)

                            ser.close()
                            phases_ini.clear()
                            phases_new.clear()
                            
                thread = threading.Thread(target=finite_loop_c)
                thread.start()


        def clear_walk_c():
            phases_new.clear()
            phases_ini.clear()
                    

        def stop_walk(*args):
            global stop_infinite, stop_fixed
            stop_infinite = True
            stop_fixed = True

        def get_speed():
            global speed_c
            speed_c = float(entry_speed.get())


        frame = CTkFrame(new_window_7)
        frame.pack()


        labelx = CTkLabel(frame, text = "Starting x coordinate:")
        labelx.grid(row = 0, column = 0)
        entryx = CTkEntry(frame)
        entryx.grid(row = 0, column = 1,pady = 5,padx = 5)

        labely = CTkLabel(frame, text = "Starting y coordinate:")
        labely.grid(row = 1, column = 0)
        entryy = CTkEntry(frame)
        entryy.grid(row = 1, column = 1, pady = 5, padx = 5)

        labelz = CTkLabel(frame, text = "Starting z coordinate:")
        labelz.grid(row = 2, column = 0)
        entryz = CTkEntry(frame)
        entryz.grid(row = 2, column = 1, pady = 5, padx = 5)

        label_step = CTkLabel(frame, text = "Step size(in degrees):") # 360/step_size = number of points (higher=smoother circle)
        label_step.grid(row = 3, column = 0)
        path_step = CTkEntry(frame)
        path_step.grid(row = 3, column = 1, pady = 5, padx = 5)

        label_axis = CTkLabel(frame, text = "Axis: horizontal, vertical(x), vertical(y):") # horizontal(z=const), vertical(x=const), vertical(y=const)
        label_axis.grid(row = 4, column = 0)
        clicked = StringVar(value = "horizontal")
        entry_axis = CTkOptionMenu(frame,
                                    values = [ "horizontal", "vertical_x", "vertical_y"],
                                    variable = clicked)
        entry_axis.grid(row = 4, column = 1, pady = 5, padx = 5)


        path_label = CTkLabel(frame, text = "Number of oscillations:") #infinite, positive integer or break
        path_label.grid(row = 5, column = 0,)
        path_entry = CTkEntry(frame)
        path_entry.grid(row = 5, column = 1, pady = 5, padx = 5)

        label_radius = CTkLabel(frame, text = "Enter path radius:")
        label_radius.grid(row = 6, column = 0,)
        entry_radius = CTkEntry(frame)
        entry_radius.grid(row = 6, column = 1, pady = 5, padx = 5)

        label_speed = CTkLabel(frame, text = "Enter speed:")
        label_speed.grid(row = 7, column = 0,)
        entry_speed = CTkEntry(frame)
        entry_speed.grid(row = 7, column = 1, pady = 5, padx = 5)
        
        run_path = CTkButton(frame, text = "Run", command = calc_points_c, fg_color = "#538e3d", hover_color="#64ab4b") 
        run_path.grid(row = 10, column = 1, pady = 5, padx = 20)

        stop_path = CTkButton(frame, text = "Stop", command = stop_walk, fg_color = "#a72828", hover_color="#cc3838")
        stop_path.grid(row = 10, column = 0, pady = 5, padx = 20)

        # Create the plot button
        plot_button = CTkButton(frame, text="Plot", command=plot_walk)
        plot_button.grid(row = 8, column = 1, pady = 5, padx = 10)

        plot_button = CTkButton(frame, text="Simulate")
        plot_button.grid(row = 8, column = 0, pady = 5, padx = 10)

        calc_button = CTkButton(frame, text="Calculate", command = run_walk)
        calc_button.grid(row = 9, column = 1, pady = 5, padx = 10)

        clear_button = CTkButton(frame, text="Clear", command = clear_walk_c)
        clear_button.grid(row = 9, column = 0, pady = 5, padx = 10)


# --------------------------------------------------------Triangular Path----------------------------------------------------------------------------


def open_new_window8():
    global initialized
    
    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
        new_window_8 = CTkToplevel(window)
        new_window_8.title('Triangular paths')
        new_window_8.resizable(False, False)
        new_window_8.geometry("+1040+100")
        
        frame = CTkFrame(new_window_8)
        frame.pack()


        # Equiliterall triangle

        def run_walk_t(*args):
            global x,y,z,step_size,base_length
            # Get input from user
            x = float(entryx.get())
            y = float(entryy.get())
            z = float(entryz.get())
            step_size = float(entry_step.get())
            base_length = float(entry_base.get())
            user_choice = path_entry.get()



            #---------------------------------------------------------------
            start = np.array((72, 72, 100))  
            end =  np.array((x, y, z))

            # Calculate the direction vector and distance between the start and end points
            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            # Generate the steps of the walk with a step size of 0.1
            steps = np.arange(0, distance + 0.4, 0.4)

            # Print the steps of the walk
            print("Steps of the walk:")
            for step in steps:
                print(np.round(start + direction * step, 2))
                calculate_phases__ini(x,y,z)
                

            #----------------END INITIALIZATION-------------------------------


            calculate_points(x,y,z,base_length)

            # Start the walk in a separate thread
            if user_choice == 'infinite':
                walk_thread = threading.Thread(target=run_infinite_t, args=(x, y, z, step_size, base_length))
                walk_thread.start()
            elif user_choice.isdigit():
                user_choice = int(user_choice)
                walk_thread = threading.Thread(target=run_fixed_t, args=(user_choice, x, y, z, step_size, base_length))
                walk_thread.start()
            else:
                raise ValueError("Invalid input. Enter 'infinite', a positive integer, or 'break'.")
            

        def run_fixed_t(user_choice, x, y, z, step_size, base_length):
            global stop_fixed
            stop_fixed = False

            for _ in range(user_choice):
                if stop_fixed:
                    break

                # Print the first step
                '''print(f"Step 1: ({x:.1f}, {y:.1f}, {z:.1f})")
                get_speed_2()
                time.sleep(speed_l)'''

                # Move the particle along the edges of the triangle and print each step
                global steps
                steps = [(x, y, z)]
                for i in range(int(base_length/step_size)):
                    x, y = next_point(x, y, 60, step_size)
                    steps.append((x, y, z))
                    #print(f"Step {i+2}: ({x:.1f}, {y:.1f}, {z:.1f})")
                    calculate_phases_new(x,y,z)
                    
                for i in range(int(base_length/step_size)):
                    x, y = next_point(x, y, 300, step_size)
                    steps.append((x, y, z))
                    #print(f"Step {i+int(base_length/step_size)+2}: ({x:.1f}, {y:.1f}, {z:.1f})")
                    calculate_phases_new(x,y,z)
                    
                for i in range(int(base_length/step_size)):
                    x, y = next_point(x, y, 180, step_size)
                    steps.append((x, y, z))
                    #print(f"Step {i+2*int(base_length/step_size)+1}: ({x:.1f}, {y:.1f}, {z:.1f})")
                    calculate_phases_new(x,y,z)

                #---------------------------------------------------------------
                start = np.array((x, y, z))  
                end =  np.array((72, 72, 100))

                # Calculate the direction vector and distance between the start and end points
                distance = np.linalg.norm(end - start)
                direction = (end - start) / distance

                # Generate the steps of the walk with a step size of 0.1
                steps = np.arange(0, distance + 0.4, 0.4)

                # Print the steps of the walk
                print("Steps of the walk:")
                for step in steps:
                    #print(np.round(start + direction * step, 2))
                    calculate_phases__man(x,y,z)

                #----------------END INITIALIZATION-------------------------------


        def stop_walk_t(*args):
            global stop_infinite
            global stop_fixed
            stop_infinite = True
            stop_fixed = True

        def run_infinite_t(x, y, z, step_size, base_length):
            global stop_infinite
            stop_infinite = False

            while not stop_infinite:

                    # Print the first step
                print(f"Step 1: ({x:.1f}, {y:.1f}, {z:.1f})")
                get_speed_2()
                time.sleep(speed_l)

                # Move the particle along the edges of the triangle and print each step
                global steps
                steps = [(x, y, z)]
                for i in range(int(base_length/step_size)):
                    x, y = next_point(x, y, 60, step_size)
                    steps.append((x, y, z))
                    print(f"Step {i+2}: ({x:.1f}, {y:.1f}, {z:.1f})")
                    get_speed_2()
                    time.sleep(speed_l)
                for i in range(int(base_length/step_size)):
                    x, y = next_point(x, y, 300, step_size)
                    steps.append((x, y, z))
                    print(f"Step {i+int(base_length/step_size)+2}: ({x:.1f}, {y:.1f}, {z:.1f})")
                    get_speed_2()
                    time.sleep(speed_l)
                for i in range(int(base_length/step_size)):
                    x, y = next_point(x, y, 180, step_size)
                    steps.append((x, y, z))
                    print(f"Step {i+2*int(base_length/step_size)+1}: ({x:.1f}, {y:.1f}, {z:.1f})")
                    get_speed_2()
                    time.sleep(speed_l)

        # Function to calculate the coordinates of the next point in the triangle path
        def next_point(x, y, angle, step_size):
            rad = math.radians(angle)
            x += step_size * math.cos(rad)
            y += step_size * math.sin(rad)
            return x, y

        def calculate_points(x, y, z, base_length):
            
            x1, y1 = x + base_length, y
            x2, y2 = x + base_length/2, y + math.sqrt(3)/2 * base_length
            x3, y3 = x, y
            return ((x1, y1, z), (x2, y2, z), (x3, y3, z))


        def plot_walk_t():

            # Visualize the path in 3D
            run_walk_t()
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            xs, ys, zs = zip(*steps)
            ax.plot(xs, ys, zs)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show()


        def get_speed_2():
            global speed_l
            speed_l = float(entry_speed_l.get())

        def calc_points_tri():
            user_choice = path_entry.get()
            ser = serial.Serial(port='COM5', baudrate=921600, timeout = 60)


            if user_choice == "infinite":
                def infinite_loop_c():
        
                    i = 0
                    data = b''
                    for i ,phase in enumerate(phases_ini):
                        data += struct.pack('>BB', i % 200, int(round(phase)))
                    ser.write(data)
                    phases_ini.clear()

                    while True:
                        i = 0
                        data = b''
                        for i ,phase in enumerate(phases_new):
                            data += struct.pack('>BB', i % 200, int(round(phase)))
                        ser.write(data)


                        if stop_infinite:
                            break
                    phases_new.clear()

                thread = threading.Thread(target=infinite_loop_c)
                thread.start()
            else:
                def finite_loop_c():
                        i = 0
                        if not phases_new:
                            print("None")
                        if not phases_ini:
                            print("None")
                        else:
                            data = b''
                            for i ,phase in enumerate(phases_ini):
                                data += struct.pack('>BB', i % 200, int(round(phase)))
                            ser.write(data)

                            for i in range(int(user_choice)):
                                for j ,phase in enumerate(phases_new):
                                    data += struct.pack('>BB', j % 200, int(round(phase)))
                                ser.write(data)

                            phases_ini.clear()
                            phases_new.clear()

                            
                thread = threading.Thread(target=finite_loop_c)
                thread.start()

            ser.close()
                    

        def clear_walk_tri():
            phases.clear()
            phases_init.clear()


        labelx = CTkLabel(frame,text = "Starting x coordinate:")
        entryx = CTkEntry(frame)
        labelx.grid(column = 0, row = 0)
        entryx.grid(column = 1, row = 0, pady = 5, padx = 5)


        labely = CTkLabel(frame, text = "Starting y coordinate:")
        entryy = CTkEntry(frame)
        labely.grid(column = 0, row = 1)
        entryy.grid(column = 1, row = 1, pady = 5, padx = 5)

        labelz = CTkLabel(frame, text = "Starting z coordinate:")
        entryz = CTkEntry(frame)
        labelz.grid(column = 0, row = 2)
        entryz.grid(column = 1, row = 2, pady = 5, padx = 5)

        label_step = CTkLabel(frame, text="Step size :")
        label_step.grid(row = 3, column = 0)
        entry_step = CTkEntry(frame)
        entry_step.grid(row = 3, column = 1, pady = 5, padx = 5)

        label_base = CTkLabel(frame,text = "Enter triangle base length:")
        entry_base = CTkEntry(frame)
        label_base.grid(column = 0, row = 4)
        entry_base.grid(column = 1, row = 4, pady = 5, padx = 5)

        path_label = CTkLabel(frame, text = "Infinite or positive integer:") 
        path_entry = CTkEntry(frame)
        path_label.grid(column = 0, row = 5)
        path_entry.grid(column = 1, row = 5,pady = 5, padx = 5)

        label_speed_l = CTkLabel(frame, text = "Enter speed:")
        label_speed_l.grid(row = 6, column = 0,)
        entry_speed_l = CTkEntry(frame)
        entry_speed_l.grid(row = 6, column = 1, pady = 5, padx = 5)


        plot_button = CTkButton(frame, text="Plot", command = plot_walk_t)
        plot_button.grid(column = 1, row = 7, pady = 10, padx = 20)

        simulate_button = CTkButton(frame, text="Simulate")
        simulate_button.grid(row = 7, column = 0, pady = 5, padx = 10)

        calculate_tri = CTkButton(frame, text = "Calculate", command = run_walk_t)
        calculate_tri.grid(column = 1, row = 8, pady = 5, padx = 20 )

        clear_path_r = CTkButton(frame, text = "Clear", command = clear_walk_tri)
        clear_path_r.grid(column = 0, row = 8, pady = 5, padx = 20)

        run_path_r = CTkButton(frame, text = "Run", fg_color = "#538e3d", hover_color="#64ab4b", command = calc_points_tri)
        run_path_r.grid(column = 1, row = 9, pady = 5, padx = 20 )

        stop_path_r = CTkButton(frame, text = "Stop",fg_color = "#a72828", hover_color="#cc3838", command = stop_walk_t )
        stop_path_r.grid(column = 0, row = 9, pady = 5, padx = 20)



# --------------------------------------------------------Rectangular Path----------------------------------------------------------------------------

def open_new_window9():

    global initialized
   
    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
        new_window_9 = CTkToplevel(window)
        new_window_9.title('Rectangular paths')
        new_window_9.resizable(False, False)
        new_window_9.geometry("+1040+100")
        
        frame = CTkFrame(new_window_9)
        frame.pack()


        def run_r(*args):
                global x,y,z
                global height
                global base_length
                global step_size
                global user_choice

                x = float(entryx.get())
                y = float(entryy.get())
                z = float(entryz.get())
                height = float(entry_hside.get())
                base_length = float(entry_lside.get())
                step_size = float(entry_step.get())

                user_choice = path_entry.get()

        #--------------------------------------------------------------------------------------------------------------------
                start = np.array((72, 72, 100))  
                end =  np.array((x, y, z))

                # Calculate the direction vector and distance between the start and end points
                distance = np.linalg.norm(end - start)
                direction = (end - start) / distance

                # Generate the steps of the walk with a step size of 0.1
                steps = np.arange(0, distance + 1, 1)


                # Print the steps of the walk
                print("Steps of the walk:")
                for step in steps:
                    x,y,z = np.round(start + direction * step, 2)
                    #print(x,y,z)
                    calculate_phases__ini(x,y,z)
                #while True:
                #   print(end)

                #----------------END INITIALIZATION-----------------------------------------------------------------------------------



                
                if user_choice == 'infinite':
                    walk_thread = threading.Thread(target=run_infinite_r, args = (x,y,z,height, base_length, step_size))
                    walk_thread.start()
                elif user_choice.isdigit():
                    user_choice = int(user_choice)
                    walk_thread = threading.Thread(target=run_fixed_r, args=(x,y,z, height, base_length,step_size, user_choice,))
                    walk_thread.start()
                else:
                    raise ValueError("Invalid input. Enter 'infinite', a positive integer, or 'break'.")

        def run_infinite_r(x, y, z, height, base_length, step_size):
            
                global stop_infinite
                stop_infinite = False
                global positions
                # Define the corners of the rectangle
                x_min, x_max = x, x + base_length
                y_min, y_max = y, y + height
                
                x_steps = np.array([step_size, 0, -step_size])
                y_steps = np.array([step_size, 0, -step_size])
                
                position = np.array([x, y, z])
                positions = [position]
                
                # Move the particle along the base of the rectangle
                while position[0] < x_max:
                    position = position + np.array([step_size, 0, 0])
                    positions.append(position)
                
                # Move the particle along the height of the rectangle
                while position[1] < y_max:
                    position = position + np.array([0, step_size, 0])
                    positions.append(position)
                
                # Move the particle back along the top of the rectangle
                while position[0] > x_min:
                    position = position + np.array([-step_size, 0, 0])
                    positions.append(position)
                
                # Move the particle back along the height of the rectangle
                while position[1] > y_min:
                    position = position + np.array([0, -step_size, 0])
                    positions.append(position)

                for position in positions:
                    #print(f"({position[0]:.2f}, {position[1]:.2f}, {position[2]:.2f})")
                    calculate_phases(int(position[0]),int(position[1]),int(position[2]))

                return positions
            

        def run_fixed_r(x, y, z, height, base_length, step_size, user_choice):
            global stop_fixed
            stop_fixed = False
            for i in range(user_choice):
                    if stop_fixed:
                        break
                    else:
                        global positions
                    
                        x_min, x_max = x, x + base_length
                        y_min, y_max = y, y + height
                        
                        x_steps = np.array([step_size, 0, -step_size])
                        y_steps = np.array([step_size, 0, -step_size])
                        
                        position = np.array([x, y, z])
                        positions = [position]
                        
                        # Move the particle along the base of the rectangle
                        while position[0] < x_max:
                            position = position + np.array([step_size, 0, 0])
                            positions.append(position)
                        
                        # Move the particle along the height of the rectangle
                        while position[1] < y_max:
                            position = position + np.array([0, step_size, 0])
                            positions.append(position)
                        
                        # Move the particle back along the top of the rectangle
                        while position[0] > x_min:
                            position = position + np.array([-step_size, 0, 0])
                            positions.append(position)
                        
                        # Move the particle back along the height of the rectangle
                        while position[1] > y_min:
                            position = position + np.array([0, -step_size, 0])
                            positions.append(position)
                        
                        

            for position in positions:
                #print(f"({position[0]:.2f}, {position[1]:.2f}, {position[2]:.2f})")

                calculate_phases_new(int(position[0]), int(position[1]), int(position[2]))
                
            return positions
            
        def stop_walk_r(*args):
            global stop_infinite
            global stop_fixed
            stop_infinite = True
            stop_fixed = True


        def plot_walk_r():
            
            run_r()
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            x_coords, y_coords, z_coords = zip(*positions)
            ax.plot(x_coords, y_coords, z_coords, '#2596be')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show()

        def calc_points_sq():
            user_choice = path_entry.get()
            ser = serial.Serial(port='COM5', baudrate=921600, timeout = 60)


            if user_choice == "infinite":
                def infinite_loop_c():
        
                    i = 0
                    data = b''
                    for i ,phase in enumerate(phases_ini):
                        data += struct.pack('>BB', i % 200, int(round(phase)))
                    ser.write(data)
                    phases_ini.clear()

                    while True:
                        i = 0
                        data = b''
                        for i ,phase in enumerate(phases_new):
                            data += struct.pack('>BB', i % 200, int(round(phase)))
                        ser.write(data)


                        if stop_infinite:
                            break
                    phases_new.clear()
                    ser.close()

                thread = threading.Thread(target=infinite_loop_c)
                thread.start()
            else:
                def finite_loop_c():
                        i = 0
                        if not phases_new:
                            print("None")
                        elif not phases_ini:
                            print("None")
                        else:
                            data = b''
                            for i, phase in enumerate(phases_ini):
                                data += struct.pack('>BB', i % 200, int(phase))
                            for i in range(int(user_choice)):
                                for i, phase in enumerate(phases_new):
                                    data += struct.pack('>BB', i % 200, int(phase))
                                ser.write(data)

                            ser.close()
                            phases_ini.clear()
                            phases_new.clear()
                            
                thread = threading.Thread(target=finite_loop_c)
                thread.start()

                    

        def clear_walk_r():
            phases.clear()
            phases_init.clear()

        def rec_speed():
            speed_r = float(speed_r_entry.get())
            time.sleep(speed_r)

        labelx = CTkLabel(frame,text = "Starting x coordinate:")
        entryx = CTkEntry(frame)
        labelx.grid(column = 0, row = 0)
        entryx.grid(column = 1, row = 0, pady = 5, padx = 5)


        labely = CTkLabel(frame, text = "Starting y coordinate:")
        entryy = CTkEntry(frame)
        labely.grid(column = 0, row = 1)
        entryy.grid(column = 1, row = 1, pady = 5, padx = 5)

        labelz = CTkLabel(frame, text = "Starting z coordinate:")
        entryz = CTkEntry(frame)
        labelz.grid(column = 0, row = 2)
        entryz.grid(column = 1, row = 2, pady = 5, padx = 5)

        label_step = CTkLabel(frame, text="Step size :")
        label_step.grid(row = 3, column = 0)
        entry_step = CTkEntry(frame)
        entry_step.grid(row = 3, column = 1, pady = 5, padx = 5)

        hside_length = CTkLabel(frame,text = "Enter side(heigth):") 
        entry_hside = CTkEntry(frame)
        hside_length.grid(column = 0, row = 4)
        entry_hside.grid(column = 1, row = 4, pady = 5, padx = 5)

        label_lside = CTkLabel(frame,text = "Enter side(base):") 
        entry_lside = CTkEntry(frame)
        label_lside.grid(column = 0, row = 5)
        entry_lside.grid(column = 1, row = 5, pady =5,padx=5)

        path_label = CTkLabel(frame, text = "Infinite or positive integer:") 
        path_entry = CTkEntry(frame)
        path_label.grid(column = 0, row = 6)
        path_entry.grid(column = 1, row = 6,pady = 5, padx = 5)

        speed_r_label = CTkLabel(frame, text = "Speed:") 
        speed_r_entry = CTkEntry(frame)
        speed_r_label.grid(column = 0, row = 7)
        speed_r_entry.grid(column = 1, row = 7,pady = 5, padx = 5)

        run_path_r = CTkButton(frame, text = "Run", command = calc_points_sq, fg_color = "#538e3d", hover_color="#64ab4b")
        run_path_r.grid(column = 1, row = 10, pady = 5, padx = 20 )

        stop_path_r = CTkButton(frame, text = "Stop", command = stop_walk_r,fg_color = "#a72828", hover_color="#cc3838" )
        stop_path_r.grid(column = 0, row = 10, pady = 5, padx = 20)

        plot_button = CTkButton(frame, text="Plot", command = plot_walk_r)
        plot_button.grid(column = 1, row = 8, pady = 5, padx = 20)

        simulate_button = CTkButton(frame, text="Simulate")
        simulate_button.grid(row = 8, column = 0, pady = 5, padx = 10)

        calc_path_r = CTkButton(frame, text = "Calculate", command = run_r)
        calc_path_r.grid(column = 1, row = 9, pady = 5, padx = 20 )

        clear_path_r = CTkButton(frame, text = "Clear", command = clear_walk_r)
        clear_path_r.grid(column = 0, row = 9, pady = 5, padx = 20)

        


 
# ----------------------------------------------------------------Spirals----------------------------------------------------------------------------


def open_new_window10():
    
    global initialized
   
    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
        new_window_10 = CTkToplevel(window)
        new_window_10.title('Spirals')
        new_window_10.resizable(False,False)
        new_window_10.geometry("+1040+100")

        # Architecture Spiral paths
        frame = CTkFrame(new_window_10)
        frame.pack()

        

        # Define spiral function
        def spiral(t):

            radius = float(radiuss_size.get())
            spiral_height = float(entry_h.get())

            x = radius * np.cos(t)
            y = radius * np.sin(t)
            z = t / (2 * np.pi) * spiral_height
            return x, y, z

        
        
        # Define a function to start the animation

        def start_animation():

            global pause_duration
            i = 0
            #pause_duration = 0.01

            x0 = float(entry_x.get())
            y0 = float(entry_y.get())
            z0 = float(entry_z.get())
            step = float(step_size.get())
            n_spirals = int(entry_n.get())


            #----------------------------------------------------------------------
            start = np.array((80, 80, 50)) 
            end =  np.array((x0, y0, z0))

            # Calculate the direction vector and distance between the start and end points
            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            # Generate the steps of the walk with a step size of 0.1
            steps = np.arange(0, distance + 0.1, 0.1)

            # Print the steps of the walk
            print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                print(x,y,z)
                #calculate_phases(x,y,z)
                time.sleep(time_speed)

            #----------------END INITIALIZATION--------------------------------------



            # Generate points along the spiral
            t = np.linspace(0, n_spirals * 2 * np.pi, int(n_spirals * 1000))
            x, y, z = spiral(t)

            # Create the full trajectory by oscillating the spiral
            trajectory = np.concatenate([np.column_stack([x, y, z]), np.column_stack([x[::-1], y[::-1], z[::-1]])])

            # Add the initial position and calculate the final position
            trajectory += [x0, y0, z0]
            final_x, final_y, final_z = trajectory[-1]

            global stop_infinite
            stop_infinite = False
            
            while not stop_infinite:
                point = trajectory[i]
                print("Step {}: ({:.2f}, {:.2f}, {:.2f})".format(i, point[0], point[1], point[2]))

                ax.clear()
                ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 'b-', linewidth=0.5)
                ax.scatter(point[0], point[1], point[2], color='g', s=100)
                ax.scatter(final_x, final_y, final_z, color='r', s=100)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                plt.draw()
                plt.pause(0.01)
                #plt.pause(0.1)
                #plt.pause(pause_duration)  # Animation doesn't work below 0.001

                i = (i + int(step * 1000)) % len(trajectory)

        def stop_animation(*args):
                global stop_infinite
                stop_infinite = True

        # Define a function to change the pause duration
        def change_pause_duration_p():
            global pause_duration
            pause_duration += 0.01

        def change_pause_duration_m():
            global pause_duration
            pause_duration -= 0.01
            
        

        label_x = CTkLabel(frame, text="Starting x coordinate:")
        label_x.grid(row=0, column=0)
        entry_x = CTkEntry(frame)
        entry_x.grid(row=0, column=1,pady =5,padx=5)

        label_y = CTkLabel(frame, text="Starting y coordinate:")
        label_y.grid(row=1, column=0)
        entry_y = CTkEntry(frame)
        entry_y.grid(row=1, column=1, pady =5,padx=5)

        label_z = CTkLabel(frame, text="Starting z coordinate:")
        label_z.grid(row=2, column=0)
        entry_z = CTkEntry(frame)
        entry_z.grid(row=2, column=1, pady =5,padx=5)



        label_n = CTkLabel(frame, text="Enter number of spirals:")
        label_n.grid(row=3, column=0)
        entry_n = CTkEntry(frame)
        entry_n.grid(row=3, column=1, pady =5,padx=5)

        label_h = CTkLabel(frame, text="Enter one spiral height:")
        label_h.grid(row=4, column=0)
        entry_h = CTkEntry(frame)
        entry_h.grid(row=4, column=1, pady =5,padx=5)


        radius_loop = CTkLabel(frame, text="Radius:")
        radius_loop.grid(row=5, column=0,)
        radiuss_size = CTkEntry(frame)
        radiuss_size.grid(row=5, column=1, pady =5,padx=5)

        step_loop = CTkLabel(frame, text="Step size:")
        step_loop.grid(row=6, column=0,)
        step_size = CTkEntry(frame)
        step_size.grid(row=6, column=1, pady =5,padx=5)


        plot_button = CTkButton(frame, text="Simulate and run", fg_color='#96be25', hover_color = "#5abe25" , command = start_animation)
        plot_button.grid(row = 7, column = 1, pady = 5, padx = 10)

        button_stop = CTkButton(frame, text="Stop", command= stop_animation)
        button_stop.grid(row=7, column=0, pady =5,padx=20)
        
        speed_up_button = CTkButton(frame, text=">>Speed up>>", command= change_pause_duration_m, fg_color="#ab2223", hover_color="#881f20")
        speed_up_button.grid(row=8, column=1, pady =5,padx=20)

        slow_down_button = CTkButton(frame, text="<<Slow down<<", command= change_pause_duration_p, fg_color="#3c881f", hover_color="#27670d")
        slow_down_button.grid(row=8, column=0, pady =5,padx=20)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')



# --------------------------------------------------------Random Path----------------------------------------------------------------------------

def open_new_window11():
    global initialized

    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
        new_window_11 = CTkToplevel(window)
        new_window_11.title('Random path')
        new_window_11.resizable(False,False)
        new_window_11.geometry("+1040+100")

      
        frame = CTkFrame(new_window_11)
        frame.pack()

        paused = False

        
        def random_walk(x0, y0, z0, step_size):
            x, y, z = x0, y0, z0
            visited = {(x0, y0, z0)}

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

           
            ax.set_xlim([0, 160])
            ax.set_ylim([0, 160])
            ax.set_zlim([0, 300])

            ax.scatter(x, y, z, color='r', marker='o')

            x_prev, y_prev, z_prev = x, y, z

            
            while True:
                while paused:
                    plt.pause(0.1)

               
                dx, dy, dz = np.random.choice([-step_size, 0, step_size], size=3)

               
                x_new, y_new, z_new = x + dx, y + dy, z + dz

             
                if (x_new, y_new, z_new) in visited:
                    continue

               
                x_prev, y_prev, z_prev = x, y, z
                x, y, z = x_new, y_new, z_new
                visited.add((x, y, z))
                print(x,y,z)
                calculate_phases_new(x,y,z)

                ax.plot([x_prev, x], [y_prev, y], [z_prev, z], color='b')
                plt.draw()
                speed_ran()
                plt.pause(speed_ran1)

   
        def start_walk():
            global paused
            paused = False
            x0 = float(entry_x.get())
            y0 = float(entry_y.get())
            z0 = float(entry_z.get())
            step_size = float(entry_step.get())

            #---------------------------------------------------------------------
            start = np.array((72, 72, 100))
            end =  np.array((x0, y0, z0))

           
            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

           
            steps = np.arange(0, distance + 0.1, 0.1)

            print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                calculate_phases__ini(x,y,z)
                time.sleep(time_speed)
            

            #----------------END INITIALIZATION--------------------------------------

            random_walk(x0, y0, z0, step_size)
        
        def run_walk():
            ser = serial.Serial(port='COM5', baudrate=921600)
            i = 0
            data = b''
            for i ,phase in enumerate(phases_ini):
                data += struct.pack('>BB', i % 200, int(phase))
            for i ,phase in enumerate(phases_new):
                data += struct.pack('>BB', i % 200, int(phase))
            ser.write(data)

            ser.close()
            phases_ini.clear()
            phases_new.clear()


            


        def pause_walk():
            global paused
            paused = True

        def resume_walk():
            global paused
            paused = False

        def clear_walk():
            phases_ini.clear()
            phases_new.clear()

        def stop_walk():
            global paused
            paused = True
            plt.close()

        def speed_ran():
            global speed_ran1
            speed_ran1 = float(speed_run_entry.get())


        label_x = CTkLabel(frame, text="Starting x coordinate:")
        label_x.grid(row=0, column=0)
        entry_x = CTkEntry(frame)
        entry_x.grid(row=0, column=1,pady =5,padx=5)

        label_y = CTkLabel(frame, text="Starting y coordinate:")
        label_y.grid(row=1, column=0)
        entry_y = CTkEntry(frame)
        entry_y.grid(row=1, column=1, pady =5,padx=5)

        label_z = CTkLabel(frame, text="Starting z coordinate:")
        label_z.grid(row=2, column=0)
        entry_z = CTkEntry(frame)
        entry_z.grid(row=2, column=1, pady =5,padx=5)

        label_length = CTkLabel(frame, text="Step size :")
        label_length.grid(row=3, column=0)
        entry_step = CTkEntry(frame)
        entry_step.grid(row=3, column=1, pady =5,padx=5)

        
        label_speed = CTkLabel(frame, text="Simulation speed:")
        label_speed.grid(row=4, column=0,)
        speed_run_entry = CTkEntry(frame)
        speed_run_entry.grid(row=4, column=1, pady =5,padx=5)

        
        button_run = CTkButton(frame, text="Run", command = start_walk) 
        button_run.grid(row=6, column=1, pady =10,padx=20)

        button_stop = CTkButton(frame, text="Stop", command = stop_walk)
        button_stop.grid(row=6, column=0, pady =5,padx=20)

       
        plot_button = CTkButton(frame, text="Resume", fg_color='#600060', hover_color = "#500050", command = resume_walk)
        plot_button.grid(row = 7, column = 0, pady = 10, padx = 10)

        plot_button = CTkButton(frame, text="Pause", fg_color='#96be25', hover_color = "#5abe25", command = pause_walk)
        plot_button.grid(row = 7, column = 1, pady = 5, padx = 10)

        run_button = CTkButton(frame, text="Run", fg_color='#96be25', hover_color = "#5abe25", command = run_walk)
        run_button.grid(row = 8, column = 1, pady = 5, padx = 10)

        clear_button = CTkButton(frame, text="Clear", command = clear_walk)
        clear_button.grid(row = 8, column = 0, pady = 5, padx = 10)





# ---------------------------------------------------------------Others----------------------------------------------------------------------------


def open_new_window12():
    global initialized
    
    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
        new_window_12 = CTkToplevel(window)
        new_window_12.title('Others')
        new_window_12.resizable(False,False)
        new_window_12.geometry("+1040+100")

        # Architecture Others
        frame = CTkFrame(new_window_12)
        frame.pack()


        label_x = CTkLabel(frame, text="Starting x coordinate:")
        label_x.grid(row=0, column=0)
        entry_x = CTkEntry(frame)
        entry_x.grid(row=0, column=1,pady =5,padx=5)

        label_y = CTkLabel(frame, text="Starting y coordinate:")
        label_y.grid(row=1, column=0)
        entry_y = CTkEntry(frame)
        entry_y.grid(row=1, column=1, pady =5,padx=5)

        label_z = CTkLabel(frame, text="Starting z coordinate:")
        label_z.grid(row=2, column=0)
        entry_z = CTkEntry(frame)
        entry_z.grid(row=2, column=1, pady =5,padx=5)

        label_length = CTkLabel(frame, text="Step size :")
        label_length.grid(row=3, column=0)
        entry_length = CTkEntry(frame)
        entry_length.grid(row=3, column=1, pady =5,padx=5)

        label_axis = CTkLabel(frame, text="Axis of movement (x, y or z):")
        label_axis.grid(row=4, column=0)
        clicked = StringVar(value = "horizontal")
        axis_select = CTkOptionMenu(frame,
                                    values = [ "horizontal", "vertical(x)", "vertical(y)"],
                                    variable = clicked)
        axis_select.grid(row=4, column=1, pady =5,padx=5)


        label_loop = CTkLabel(frame, text="Number of oscillations:") #(infinite, positive integer or break):
        label_loop.grid(row=5, column=0,)
        entry_loop = CTkEntry(frame)
        entry_loop.grid(row=5, column=1, pady =5,padx=5)

        button_type = CTkLabel(frame, text= 'Others')
        button_type.grid(row = 6, column = 0, pady=5, padx=5)

        button_entry = CTkEntry(frame)
        button_entry.grid(row=6, column = 1, pady = 5, padx = 5)

        
        button_run = CTkButton(frame, text="Run") 
        button_run.grid(row=7, column=1, pady =10,padx=20)

        button_stop = CTkButton(frame, text="Stop")
        button_stop.grid(row=8, column=1, pady =5,padx=20)

        # Create the plot button
        plot_button = CTkButton(frame, text="Plot", fg_color='#600060', hover_color = "#500050")
        plot_button.grid(row = 7, column = 0, pady = 10, padx = 10)

        plot_button = CTkButton(frame, text="Simulate", fg_color='#96be25', hover_color = "#5abe25")
        plot_button.grid(row = 8, column = 0, pady = 5, padx = 10)


    #------------------------------------------------------------------Linear Walk----------------------------------------------------------------------
    # 2 oscilation means the walk to and fro
    # probalbe problems with printing the last step in loop (the user entries)


def open_new_window13():
    global initialized
    global phases_ini
    global phases_new
    
    if not initialized:
        messagebox.showwarning("Initialization warning","Particle has not been yet initialized. Run initialize button first")
    else:
   

        def particle_walk(start_x, start_y, start_z, path_length, axis, stepsize):
            x = start_x
            y = start_y
            z = start_z
            st = stepsize
            steps = int(path_length / st)
            positions = []


            for i in range(steps):
                if axis == 'x':
                    x += st
                elif axis == 'y':
                    y += st
                elif axis == 'z':
                    z += st
                else:
                    raise ValueError("Invalid axis. Choose 'x', 'y' or 'z'.")
                positions.append((x, y, z))
            return positions

        def run_walk(*args):
            start_x = float(entry_x.get())
            start_y = float(entry_y.get())
            start_z = float(entry_z.get())
            path_length = float(entry_length.get())
            axis = axis_select.get()
            stepsize = float(step_size.get())

            #------------------------------------------------------------
            start = np.array((72, 72, 100)) 
            end =  np.array((start_x, start_y, start_z))

           
            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

         
            steps = np.arange(0, distance + 0.2, 0.2)

   
            print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                #print(x,y,z)
                calculate_phases__ini(x,y,z)

            #----------------END INITIALIZATION----------------------------



            positions = particle_walk(start_x, start_y, start_z, path_length, axis, stepsize)
            user_choice = entry_loop.get()
            if user_choice == 'infinite':
                walk_thread = threading.Thread(target=run_infinite_walk, args=(positions,))
                walk_thread.start()
            elif user_choice.isdigit():
                user_choice = int(user_choice)
                walk_thread = threading.Thread(target=run_fixed_walk, args=(positions, user_choice))
                walk_thread.start()
            else:
                raise ValueError("Invalid input. Enter 'infinite', a positive integer, or 'break'.")
            
        def run_infinite_walk(positions):
            global stop_infinite
            stop_infinite = False
            for j, pos in enumerate(positions):
                #print("Step {}: ({:.1f}, {:.1f}, {:.1f})".format(j + 1, pos[0], pos[1], pos[2]))
                calculate_phases_new(int(pos[0]), int(pos[1]), int(pos[2]))
            positions = positions[::-1]

        def run_fixed_walk(positions, user_choice):
            global stop_fixed
            stop_fixed = False
            for i in range(user_choice):
                if stop_fixed:
                    break
                for j, pos in enumerate(positions):
                    #print("Step {}: ({:.1f}, {:.1f}, {:.1f})".format(j + 1, pos[0], pos[1], pos[2]))
                    calculate_phases_new(int(pos[0]), int(pos[1]), int(pos[2]))
                    if stop_fixed:
                        break
                print("calculated")
                positions = positions[::-1]
            

                
        ''' #------------------------------------------------------------
            start = np.array(positions[0])  
            end =  np.array((72, 72, 100))

            # Calculate the direction vector and distance between the start and end points
            distance = np.linalg.norm(end - start)
            direction = (end - start) / distance

            # Generate the steps of the walk with a step size of 0.1
            steps = np.arange(0, distance + 0.1, 0.1)

            # Print the steps of the walk
            print("Steps of the walk:")
            for step in steps:
                x,y,z = np.round(start + direction * step, 2)
                print(x,y,z)
                calculate_phases_new(x,y,z)
                

            #----------------END INITIALIZATION----------------------------'''

       
        def calc_points_lin():
            user_choice = entry_loop.get()
            ser = serial.Serial(port='COM5', baudrate=921600, timeout = 120)

            if user_choice == "infinite":
                def infinite_loop():
                  
                    i = 0

                    data = b''
                    for i, phase in enumerate(phases_ini):
                        data += struct.pack('>BB', i % 200, int(phase))
                    ser.write(data)
                    ser.close()
                    phases_ini.clear()
                   
                    while True:
                        '''data = b'''''
                        for i, phase in enumerate(phases_new):
                            data += struct.pack('>BB', i % 200, int(phase))
                            ser.write(data)
                        
                        
                        if stop_infinite:
                            break
                    ser.close()
                    phases_new.clear()

                thread = threading.Thread(target=infinite_loop)
                thread.start()
            else:
                def finite_loop():
                    i = 0
                    if not phases_new:
                        print("None")
                    elif not phases_ini:
                        print("None")
                    else:
                        data = b''
                        for i, phase in enumerate(phases_ini):
                            data += struct.pack('>BB', i % 200, int(phase))
                        for i, phase in enumerate(phases_new):
                            data += struct.pack('>BB', i % 200, int(phase))
                        ser.write(data)
                        ser.close()
                        phases_ini.clear()
                        phases_new.clear()

                thread = threading.Thread(target=finite_loop)
                thread.start()
            


        def clear_walk_l():
            phases_new.clear()
            phases_init.clear()

        def stop_walk(*args):
            global stop_infinite
            global stop_fixed
            stop_infinite = True
            stop_fixed = True

        

        def collect_walk_data():
            start_x = float(entry_x.get())
            start_y = float(entry_y.get())
            start_z = float(entry_z.get())
            path_length = float(entry_length.get())
            axis = axis_select.get()
            stepsize = float(step_size.get())
            positions = particle_walk(start_x, start_y, start_z, path_length, axis, stepsize)
            return positions

        def plot_walk(positions):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            xs = [pos[0] for pos in positions]
            ys = [pos[1] for pos in positions]
            zs = [pos[2] for pos in positions]
            ax.plot(xs, ys, zs)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('Particle Walk')
            plt.show()


        def collect_and_plot_walk_data():
            positions = collect_walk_data()
            plot_walk(positions)

        def speed_lin():
            global speed_s
            speed_s = float(entry_speed_s.get())
            


       
        new_window_13 = CTkToplevel(window)
        new_window_13.title('Linear path')
        new_window_13.resizable(False,False)
        new_window_13.geometry("+1040+100")


        frame = CTkFrame(new_window_13)
        frame.pack()


        label_x = CTkLabel(frame, text="Starting x coordinate:")
        label_x.grid(row=0, column=0)
        entry_x = CTkEntry(frame)
        entry_x.grid(row=0, column=1,pady =5,padx=5)

        label_y = CTkLabel(frame, text="Starting y coordinate:")
        label_y.grid(row=1, column=0)
        entry_y = CTkEntry(frame)
        entry_y.grid(row=1, column=1, pady =5,padx=5)

        label_z = CTkLabel(frame, text="Starting z coordinate:")
        label_z.grid(row=2, column=0)
        entry_z = CTkEntry(frame)
        entry_z.grid(row=2, column=1, pady =5,padx=5)

        label_length = CTkLabel(frame, text="Path length:")
        label_length.grid(row=3, column=0)
        entry_length = CTkEntry(frame)
        entry_length.grid(row=3, column=1, pady =5,padx=5)

        label_axis = CTkLabel(frame, text="Axis of movement (x, y or z):")
        label_axis.grid(row=4, column=0)
        clicked = StringVar(value = "x")
        axis_select = CTkOptionMenu(frame,
                                    values = [ "x", "y", "z"],
                                    variable = clicked)
        axis_select.grid(row=4, column=1, pady =5,padx=5)


        label_loop = CTkLabel(frame, text="Number of oscillations:")
        label_loop.grid(row=5, column=0,)
        entry_loop = CTkEntry(frame)
        entry_loop.grid(row=5, column=1, pady =5,padx=5)

        step_loop = CTkLabel(frame, text="Step size:")
        step_loop.grid(row=6, column=0,)
        step_size = CTkEntry(frame)
        step_size.grid(row=6, column=1, pady =5,padx=5)

        speed_loop = CTkLabel(frame, text="Speed:")
        speed_loop.grid(row=7, column=0,)
        entry_speed_s = CTkEntry(frame)
        entry_speed_s.grid(row=7, column=1, pady =5,padx=5)

        
        button_run = CTkButton(frame, text="Calculate", command= run_walk) 
        button_run.grid(row=9, column=1, pady =10,padx=20)

        button_stop = CTkButton(frame, text="Clear", command = clear_walk_l)
        button_stop.grid(row=9, column=0, pady =5,padx=20)

        plot_button = CTkButton(frame, text="Plot", command= collect_and_plot_walk_data)
        plot_button.grid(row = 8, column = 1, pady = 10, padx = 10)

        plot_button = CTkButton(frame, text="Simulate")
        plot_button.grid(row = 8, column = 0, pady = 5, padx = 10)


        run_path_r = CTkButton(frame, text = "Run", fg_color = "#538e3d", hover_color="#64ab4b", command = calc_points_lin)
        run_path_r.grid(column = 1, row = 10, pady = 5, padx = 20 )

        stop_path_r = CTkButton(frame, text = "Stop", command = stop_walk,fg_color = "#a72828", hover_color="#cc3838" )
        stop_path_r.grid(column = 0, row = 10, pady = 5, padx = 20)



#----------------------- x,y,z, entiery functions -------------------------


#initialize x+
def xp():    
    if step_size == "":
        print("Step size must be a value!")
    elif entryy == "":
        print("Y value must be entered!")
    elif entryz =="":
        print("Z value must be entered!")
    else:
        new_entry_x = (float(entryx.get()) - float(step_entry.get()))
        new_entry_x = round(new_entry_x , 4)
        
    entryx.delete(0, END)
    
    entryx.insert(0, new_entry_x)
    xvalue  = entryx.get()
    yvalue = entryy.get()
    zvalue = entryz.get()
    print(xvalue, yvalue, zvalue)
    calculate_phases__man(float(xvalue),float(yvalue),float(zvalue))
    

#initialize x-
def xm():    
    if step_size == "":
        print("Step size must be a value!")
    elif entryy == "":
        print("Y value must be entered!")
    elif entryz =="":
        print("Z value must be entered!")
    else:
        new_entry_x = (float(entryx.get()) + float(step_entry.get()))
        new_entry_x = round(new_entry_x , 4)
        
    entryx.delete(0, END)
    
    entryx.insert(0, new_entry_x)

    xvalue  = entryx.get()
    yvalue = entryy.get()
    zvalue = entryz.get()
    print(xvalue, yvalue, zvalue)
    calculate_phases__man(float(xvalue),float(yvalue),float(zvalue))
    

#initialize y+
def yp():    
    if step_size == "":
        print("Step size must be a value!")
    elif entryy == "":
        print("Y value must be entered!")
    elif entryz =="":
        print("Z value must be entered!")
    else:
        new_entry_y = (float(entryy.get()) - float(step_entry.get()))
        new_entry_y = round(new_entry_y , 4)
        
    entryy.delete(0, END)
    
    entryy.insert(0, new_entry_y)
    
    xvalue  = entryx.get()
    yvalue = entryy.get()
    zvalue = entryz.get()
    print(xvalue, yvalue, zvalue)
    calculate_phases__man(float(xvalue),float(yvalue),float(zvalue))

#initialize y-
def ym():    
    if step_size == "":
        print("Step size must be a value!")
    elif entryy == "":
        print("Y value must be entered!")
    elif entryz =="":
        print("Z value must be entered!")
    else:
        new_entry_y = (float(entryy.get()) + float(step_entry.get()))
        new_entry_y = round(new_entry_y , 4)
        
    entryy.delete(0, END)
    
    entryy.insert(0, new_entry_y)
    
    xvalue  = entryx.get()
    yvalue = entryy.get()
    zvalue = entryz.get()
    print(xvalue, yvalue, zvalue)
    calculate_phases__man(float(xvalue),float(yvalue),float(zvalue))

#initialize z-
def zm():    
    if step_size == "":
        print("Step size must be a value!")
    elif entryy == "":
        print("Y value must be entered!")
    elif entryz =="":
        print("Z value must be entered!")
    else:
        new_entry_z = (float(entryz.get()) - float(step_entry.get()))
        new_entry_z = round(new_entry_z , 4)
        
    entryz.delete(0, END)
    
    entryz.insert(0, new_entry_z)
    
    xvalue  = entryx.get()
    yvalue = entryy.get()
    zvalue = entryz.get()
    print(xvalue, yvalue, zvalue)
    calculate_phases__man(float(xvalue),float(yvalue),float(zvalue))


#initialize z+
def zp():    
    if step_size == "":
        print("Step size must be a value!")
    elif entryy == "":
        print("Y value must be entered!")
    elif entryz =="":
        print("Z value must be entered!")
    else:
        new_entry_z = (float(entryz.get()) + float(step_entry.get()))
        new_entry_z = round(new_entry_z , 4)
        
    entryz.delete(0, END)
    
    entryz.insert(0, new_entry_z)
    
    xvalue  = entryx.get()
    yvalue = entryy.get()
    zvalue = entryz.get()
    print(xvalue, yvalue, zvalue)
    calculate_phases__man(float(xvalue),float(yvalue),float(zvalue))

#---------------------------------------------------------------------END-----------------------------------------------------------------------------




        


style.configure('TButton', font=("Verdana", 10)) 
buttonxp = CTkButton(tab1, text="X+",width=50, command=lambda: (move_right(), xp()))# xp - x+
buttonxm = CTkButton(tab1, text="X-",width=50, command= lambda: (move_left(), xm()))# xm - x-
buttonyp = CTkButton(tab1, text="Y+",width=50, command= lambda: (move_forward(), yp()))
buttonym= CTkButton(tab1, text="Y-",width=50, command= lambda: (move_backward(), ym()))
buttonzp = CTkButton(tab1, text="Z+",width=50, command= lambda: (move_up(), zp()))
buttonzm = CTkButton(tab1, text="Z-",width=50, command= lambda: (move_down(), zm()))

# Buttons manual entry
labelx = CTkLabel(tab1, text = 'X', text_color = 'red', font = ('Arial',20))
labely = CTkLabel(tab1, text = 'Y',text_color = 'green',font = ('Arial',20))
labelz = CTkLabel(tab1, text = 'Z',text_color = 'blue',font = ('Arial',20))
#labelmm1 = CTkLabel(tab1, text = '[mm]',text_color = 'white',font = ('Arial',10))
#labelmm2 = CTkLabel(tab1, text = '[mm]',text_color = 'white',font = ('Arial',10))
#labelmm3 = CTkLabel(tab1, text = '[mm]',text_color = 'white',font = ('Arial',10))

class OptionMenuButton:
    def __init__(self, master, values, variable, width, button_color, fg_color, button_hover_color):
        self.optionmenu_unit = StringVar(value="[mm]") # set initial value
        self.unit_option = CTkOptionMenu(master=master,
                                         values=values,
                                         variable=variable,
                                         width=width,
                                         button_color=button_color,
                                         fg_color=fg_color,
                                         button_hover_color=button_hover_color)
        self.unit_option.pack()

button1 = OptionMenuButton(tab1, ["[mm]", "[cm]", "[m]"], StringVar(value="[mm]"), 10, '#6e727c', '#54575d', '#6e727c')
button2 = OptionMenuButton(tab1, ["[mm]", "[cm]", "[m]"], StringVar(value="[mm]"), 10, '#6e727c', '#54575d', '#6e727c')
button3 = OptionMenuButton(tab1, ["[mm]", "[cm]", "[m]"], StringVar(value="[mm]"), 10, '#6e727c', '#54575d', '#6e727c')

button1.unit_option.place(x=190,y=30)
button2.unit_option.place(x=190,y=80)
button3.unit_option.place(x=190,y=130)


labelx.place(x=20,y=30)
labely.place(x=20,y=80)
labelz.place(x=20,y= 130)


# Buttons entry

def clickx():
    xvalue  = entryx.get()
    yvalue = entryy.get()
    zvalue = entryz.get()
    print(xvalue, yvalue, zvalue)

def clicky():
    yvalue  = entryy.get()
    print(yvalue)

def clickz():
    zvalue  = entryz.get()
    print(zvalue)




entryx = CTkEntry(tab1, width = 130)
entryy = CTkEntry(tab1, width = 130)
entryz = CTkEntry(tab1, width = 130)
#buttonl = CTkButton(tab1, text = 'Load',fg_color='#2d2d30',border_color = '#007acc',border_width = 2,font = ('Arial',20), width = 70, height = 70, command=lambda: [clickx(), clicky(),clickz()])

entryx.place(x=50,y=30)
entryy.place(x=50, y=80)
entryz.place(x=50, y=130)


'''
def config_entries():
    initial_value = "150"
    initial_val = tk.StringVar(value=initial_value)

    entryx.configure( textvariable = initial_val)
    entryy.configure( textvariable = initial_val)
    entryz.configure( textvariable = initial_val)
'''

buttonxp.place(x=180, y=230)
buttonxm.place(x=40,y=230)
buttonyp.place(x=110,y=190)
buttonym.place(x=110,y=230)
buttonzp.place(x=180, y=190)
buttonzm.place(x=40, y=190)






step_size = CTkLabel(tab1, text = "Step size", width = 60,font = ('Verdana',13))
step_size.place(x=40,y=280)
step_entry = CTkEntry(tab1, width = 120)
step_entry.place(x=110, y=280)

fl_step =step_entry.get()


# Initialize button

initbutton = CTkButton(tab1, text = "Initialize", width = 200, height = 40, command = initialize_s, fg_color="#93a70a", font = ("Verdana", 18))
initbutton.configure(hover_color= "#9ead31")
initbutton.place(x = 40, y = 370)


optionmenu_var_fpga = StringVar(value=" Chained FPGA")  # set initial value

def optionmenu_fpga(choice):
    print("optionmenu dropdown clicked:", choice)

fpgabox = CTkOptionMenu(master=tab1,
                                       values=["Chained FPGA"],
                                       command=optionmenu_fpga,
                                       variable=optionmenu_var_fpga,
                                       fg_color="#54575d",
                                       button_color="#6e727c",
                                       button_hover_color = "#6e727c",
                                       width = 200,
                                       font = ('Verdana',13))
fpgabox.place(x = 40 ,y = 630)


traps_inf = CTkButton(tab1, text= "Traps", width = 150, font = ('Verdana',13), fg_color = "#32a887", hover_color = "#43debc" )
traps_inf.place(x=40, y=430)

pressure_inf = CTkButton(tab1, text= "Pressure", width = 150, font = ('Verdana',13), fg_color = "#32a887", hover_color = "#43debc" )
pressure_inf.place(x=40, y=480)

Phase_inf = CTkButton(tab1, text= "Phase", width = 150, font = ('Verdana',13), fg_color = "#32a887", hover_color = "#43debc" )
Phase_inf.place(x=40, y=530)


amp_inf = CTkButton(tab1, text= "Amplitude", width = 150, font = ('Verdana',13), fg_color = "#32a887", hover_color = "#43debc" )
amp_inf.place(x=40, y=580)


from tkinter import colorchooser

class ColorPickerApp:
    def __init__(self, master):
        self.master = master
        #master.title("Color Picker App")

        self.color_label = CTkLabel(master, text="Sphere color")
        self.color_label.place(x=40,y=680)

        self.color_button = CTkButton(master, text="",
                                      command=self.show_color_picker ,
                                      width = 60,
                                      fg_color="white",
                                      hover_color="white")
        self.color_button.place(x=140, y=680)

        self.selected_color = None

    def show_color_picker(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color_button.configure(fg_color=color, hover_color = color)
            self.selected_color = color

    def get_selected_color(self):
        return self.selected_color

app = ColorPickerApp(tab1)


radius_size_s = CTkLabel(tab1, text = "Sphare radius", width = 60,font = ('Verdana',13))
radius_size_s.place(x=40,y=720)
radius_s_entry = CTkEntry(tab1, width = 60)
radius_s_entry.place(x=140, y=720)



# Global time variable (levitation speed)

time_speed = 0
time_label = CTkLabel(tab1, text = "Speed", width = 60,font = ('Verdana',13))
time_label.place(x=40,y=320)
time_entry = CTkEntry(tab1, width = 120)
time_entry.place(x=110, y=320)
'''def get_time_speed():
    global time_speed
    time_speed = float(time_entry.get())'''



# Initialize images tab2

img1 = Image.open('zdjęcia/g1.png')
img1RImage = ImageTk.PhotoImage(img1.resize((130,130), Image.ANTIALIAS))
lg1 = Label(tab2,image = img1RImage)

img2 = Image.open('zdjęcia/g2.png')
img2RImage = ImageTk.PhotoImage(img2.resize((130,130), Image.ANTIALIAS))
lg2 = Label(tab2,image = img2RImage)

img3 = Image.open('zdjęcia/g3.png')
img3RImage = ImageTk.PhotoImage(img3.resize((130,130), Image.ANTIALIAS))
lg3 = Label(tab2,image = img3RImage)

img4 = Image.open('zdjęcia/g4.png')
img4RImage = ImageTk.PhotoImage(img4.resize((130,130), Image.ANTIALIAS))
lg4 = Label(tab2,image = img4RImage)

img5 = Image.open('zdjęcia/g5.png')
img5RImage = ImageTk.PhotoImage(img5.resize((130,130), Image.ANTIALIAS))
lg5 = Label(tab2,image = img5RImage)

img6 = Image.open('zdjęcia/g6.png')
img6RImage = ImageTk.PhotoImage(img6.resize((130,130), Image.ANTIALIAS))
lg6 = Label(tab2,image = img6RImage)

img7 = Image.open('zdjęcia/g7.png')
img7RImage = ImageTk.PhotoImage(img7.resize((130,130), Image.ANTIALIAS))
lg7 = Label(tab2,image = img7RImage)


button7 = CTkButton(tab2, 
                    text="Circular paths",
                    font=("Arial", 13 ),
                    hover= True,
                    hover_color= "#159947",
                    width= 110,
                    border_width=2,
                    border_color= "#608a4d", 
                    bg_color="#262626",
                    fg_color= "#79ae61",
                    command=open_new_window7)
button8 = CTkButton(tab2,
                    text="Triangular paths",
                    font=("Arial", 13 ),
                    hover= True,
                    hover_color= "#159947",
                    width= 110,
                    border_width=2,
                    border_color= "#608a4d", 
                    bg_color="#262626",
                    fg_color= "#79ae61",
                    command=open_new_window8)
button9 = CTkButton(tab2, 
                    text="Rectangular paths",
                    font=("Arial", 13 ),
                    hover= True,
                    hover_color= "#159947",
                    width= 110,
                    border_width=2,
                    border_color= "#608a4d", 
                    bg_color="#262626",
                    fg_color= "#79ae61", 
                    command=open_new_window9)
button10 = CTkButton(tab2, 
                    text="Spirals",
                    font=("Arial", 13 ),
                    hover= True,
                    hover_color= "#159947",
                    width= 110,
                    border_width=2,
                    border_color= "#608a4d", 
                    bg_color="#262626",
                    fg_color= "#79ae61",
                    command=open_new_window10)
button11= CTkButton(tab2,
                    text="Random path",
                    font=("Arial", 13 ),
                    hover= True,
                    hover_color= "#159947",
                    width= 110,
                    border_width=2,
                    border_color= "#608a4d", 
                    bg_color="#262626",
                    fg_color= "#79ae61",
                    command=open_new_window11)
button12= CTkButton(tab2,
                    text="Others",
                    font=("Arial", 13 ),
                    hover= True,
                    hover_color= "#159947",
                    width= 110,
                    border_width=2,
                    border_color= "#608a4d", 
                    bg_color="#262626",
                    fg_color= "#79ae61",
                    command=open_new_window12)
button13= CTkButton(tab2,
                    text="Linear path",
                    font=("Arial", 13 ),
                    hover= True,
                    hover_color= "#159947",
                    width= 110,
                    border_width=2,
                    border_color= "#608a4d", 
                    bg_color="#262626",
                    fg_color= "#79ae61",
                    command=open_new_window13) # trzeba zrobic klase zeby nie powtarzac


button13.place(x=20,y=20)
lg1.place(x=190, y=28)

button7.place(x=150,y=142)
lg2.place(x=20, y=126)

button8.place(x=20,y=256)
lg3.place(x=190, y = 272)

button9.place(x=150,y=370)
lg4.place(x = 20, y = 420)

button10.place(x=20,y=484)
lg5.place(x=190, y=560)

button11.place(x=150,y=598)
lg6.place(x = 20, y=700)

button12.place(x=20,y=712)
lg7.place(x = 190, y=800)



def on_closing():
    window.destroy()
    pygame.quit()




window.protocol("WM_DELETE_WINDOW", on_closing)


window.mainloop()
