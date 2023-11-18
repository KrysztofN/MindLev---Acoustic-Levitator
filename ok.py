import math
import struct
import serial
import time


#ser = serial.Serial(port='COM3', baudrate=921600)

phases_new = []
phases_ini = []

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

class Transducer:
    def __init__(self, pt, isOnTop):
        self.pt = pt
        self.isOnTop = isOnTop
        self.focusedPhase = None
        
class SImPoints:
    def __init__(self):
        self.transducers = []
        
    def addTransducer(self, pt, isOnTop):
        self.transducers.append(Transducer(pt, isOnTop))
        
    def calculatePhase(self, obj_pos):
        global PIEZO_FREQ
        WAVE_C = 343000
        PIEZO_FREQ = 40000
        WAVE_K = 2*math.pi*PIEZO_FREQ/WAVE_C

        for t in range(len(self.transducers)):
            delta = obj_pos - self.transducers[t].pt
            r = delta.length()
            s = -r*WAVE_K
            if self.transducers[t].isOnTop:
                s += math.pi

            self.transducers[t].focusedPhase = math.fmod(s, 2*math.pi) + 2*math.pi



sim_points = SImPoints()

for i in range(10):
    for j in range(10):
        if i < 5:
            pt = Vector3D(j*16, (9-i)*16, 0)
        else:
            pt = Vector3D(j*16, (9-i)*16, 0)
        isOnTop = False
        sim_points.addTransducer(pt, isOnTop)

for i in range(10):
    for j in range(10):
        if i < 5:
            pt = Vector3D(j*16, (9-i)*16, 200)
        else:
            pt = Vector3D(j*16, (9-i)*16, 200)
        isOnTop = True
        sim_points.addTransducer(pt, isOnTop)


        
#obj_pos = Vector3D(72, 72, 100)

def calculate_phases_new(x, y, z):
    global sim_points, phases_new
    
    obj_pos = Vector3D(x, y, z)
    sim_points.calculatePhase(obj_pos)

    i = 0 
    for t in sim_points.transducers:
        phase_us = t.focusedPhase / (2*math.pi*PIEZO_FREQ) * 1e6
        phase_us = round(phase_us/0.5,0)
        phases_new.append(phase_us)
        #print(phase_us)

        '''num = struct.pack('>B', int(i))
        ser.write(num)
        result_send = struct.pack('>B', int(phase_us))
        ser.write(result_send)'''
        #print(f"Transducer at ({t.pt.x}, {t.pt.y}, {t.pt.z}): {phase_us:.2f} "+ "   "+ str(i))
        i += 1


def calculate_phases__ini(x, y, z):
    global sim_points, phases_ini
    
    obj_pos = Vector3D(x, y, z)
    sim_points.calculatePhase(obj_pos)

    i = 0 
    for t in sim_points.transducers:
        phase_us = t.focusedPhase / (2*math.pi*PIEZO_FREQ) * 1e6
        phase_us = round(phase_us/0.5,0)
        phases_ini.append(phase_us)
       


        '''num = struct.pack('>B', int(i))
        ser.write(num)
        result_send = struct.pack('>B', int(phase_us))
        ser.write(result_send)'''
        #print(f"Transducer at ({t.pt.x}, {t.pt.y}, {t.pt.z}): {phase_us:.2f} "+ "   "+ str(i))
        i += 1



def calculate_phases__man(x, y, z):
    global sim_points, phases_ini
    ser = serial.Serial(port='COM5', baudrate=921600)
    
    obj_pos = Vector3D(x, y, z)
    sim_points.calculatePhase(obj_pos)

    # Print the focused phase of each transducer in microseconds
    i = 0 
    for t in sim_points.transducers:
        phase_us = t.focusedPhase / (2*math.pi*PIEZO_FREQ) * 1e6
        phase_us = round(phase_us/0.5,0)
        phases_ini.append(phase_us)
       

        
        num = struct.pack('>B', int(i))
        ser.write(num)
        result_send = struct.pack('>B', int(phase_us))
        ser.write(result_send)
        i += 1
    ser.close

'''calculate_phases_new(72,72,100)
calculate_phases_new(72,72,112)

data = b''
for i, phase in enumerate(phases_ini):
    data += struct.pack('>BB', i % 200, int(phase))
for i, phase in enumerate(phases_new):
    data += struct.pack('>BB', i % 200, int(phase))
ser.write(data)
ser.close()
'''
