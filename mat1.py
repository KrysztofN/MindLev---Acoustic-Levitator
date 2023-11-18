import math
import struct
import serial
import time

#ser = serial.Serial(port='COM3', baudrate=921600)
phases_init = []
transducers = []
i=0
def calculate_phases_init(xcc,ycc,zcc):
    Xc = xcc
    Yc = ycc
    Zc = zcc
    xg = 0 #xglosnika
    yg = 0#yglosnika
    H = 200 #wysokość lewitatora [mm]


    def funkcja_dol_init(xg,yg):
            global result
            result = (((((math.sqrt(((Xc-xg)**2+(Yc-yg)**2)+Zc**2)-Zc)*100/34) % 25) - (((((math.sqrt(((Xc-xg)**2+(Yc-yg)**2)+Zc**2)-Zc)*100/34) % 25)//0.5) * 0.5)) //0.25) + ((((math.sqrt(((Xc-xg)**2+(Yc-yg)**2)+Zc**2)-Zc)*100/34) % 25)//0.5) + 1
            #print('głośnik', i + 1, ' --dół')
            #print(result) #funkcja_dol obliczajaca kanał
            #result_send = struct.pack('>B', int(result))
            #ser.write(result_send)
            phases_init.append(int(result))
            
    X = 8
    Y = 8

    def funkcja_gora_init(xg,yg):
            global result
            result = (((((math.sqrt(((Xc-xg)**2+(Yc-yg)**2)+(H-Zc)**2)-(H-Zc))*100/34) % 25) - (((((math.sqrt(((Xc-xg)**2+(Yc-yg)**2)+(H-Zc)**2)-(H-Zc))*100/34) % 25)//0.5) * 0.5)) //0.25) + ((((math.sqrt(((Xc-xg)**2+(Yc-yg)**2)+(H-Zc)**2)-(H-Zc))*100/34) % 25)//0.5) + 1
            #print('głośnik', d + 1, ' --góra')
            #print(result)
            #result_send = struct.pack('>B', int(result))
            #ser.write(result_send)
            phases_init.append(int(result))
            
    X = 8
    Y = 8


    for i in range(100): #zapetlenie funkcji i kolejne przypisywanie pozycji glosnikow
            
        if i > 0:
            X += 16
                    

        if X > 152:
            X = 8
            Y += 16
        if Y > 152:
            Y = 8

        funkcja_dol_init(X,Y)

    for d in range(100): #zapetlenie funkcji i kolejne przypisywanie pozycji glosnikow
            
        if d > 0:
            X += 16
                    

        if X > 152:
            X = 8
            Y += 16
        if Y > 152:
            Y = 8

        funkcja_gora_init(X,Y)

#calculate_phases_init(79,79,51)
