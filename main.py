import serial
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import subprocess as sp 
from os import system
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


def run():

    try:
        myser = Iserial(searchPorts(), 115200)
        hasSerial = True
    except:
        hasSerial = False

    while True:
        try:
            system('cls')#Solo windows
        except:
            pass

        print(f'''\t\tIserial\n\n
    Los puertos seriales actuales son:
    {hasSerial}
    {searchPorts()}

    [I]nit. solo si existe puerto serial.
    [L]eer
    [E]scribir
    [S]alir
            ''')
        opc = str(input('Ingresar opc: ')).upper()
        if opc == 'I' and hasSerial == False:
            myser = Iserial(searchPorts(), 115200)
            hasSerial = True
        elif opc == 'L' and hasSerial:  
            myser.run()
        elif opc == 'E' and hasSerial:
            byte = bytes(str(input('Ingrese byte: ')), 'utf-8')
            myser.writeByte(byte)
        elif opc == 'S':
            break
        else:
            print('Ha dijitado erroneamente')
            print('O no se ha inicializado el serial')

if __name__ == "__main__":
    run()
