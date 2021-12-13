import serial
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import subprocess as sp 
#interval es el valor de la psoc de delay/4

def searchPorts():
    ports = sp.check_output(['py', '-m', 'serial.tools.list_ports'])
    ports = ports.decode('utf-8')
    ports = ports.strip()
    return ports

def bytesToString(listOfBytes):
    return float(''.join([k.decode('utf-8') for k in listOfBytes]))



class Iserial:
    def __init__(self, port, bauding):
        self._ser = serial.Serial(port, bauding)

        self.initConfigurations(100,1.2,0)

    def initConfigurations(self, max_x, max_rand, min_rand):
        self._fig, ax = plt.subplots()
        x = np.arange(0, max_x)
        subx = np.arange(0, max_x)
        ax.set_ylim(min_rand, max_rand)
        self._line, = ax.plot(x, subx)
        self._imagen = [np.nan] * len(x)
#        print(self._line)
#        print(type(self._line))

    def writeByte(self, byte:bytes):
        self._ser.write( byte )

    def run(self):
        self.writeByte(b'2')
        ani = FuncAnimation( self._fig, self.animate, init_func=self.first, interval=5, blit=True, save_count=10)
        plt.show()
        self.writeByte(b'1')
        plt.close()

    def animate(self, frame):
        data = []
        for i in range(4):
            some = self._ser.read()
            data.append( some )
        print( bytesToString(data) )
        self._imagen.append( bytesToString(data) )
        self._imagen.pop(0)   
        
        self._line.set_ydata(self._imagen)

        return (self._line,)

    def first(self):
        self._line.set_ydata( self._imagen )
        return (self._line,)



if __name__ == "__main__":

    myser = Iserial(searchPorts(), 115200)
    myser.run()