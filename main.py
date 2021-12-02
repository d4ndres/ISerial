import serial
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def bytesToString(listOfBytes):
    return float(''.join([k.decode('utf-8') for k in listOfBytes]))


def init():
    line.set_ydata( imagen )
    return line,


def animate(frame): 

    data = []
    for i in range(4):
        some = ser.read()
        data.append( some )
    print( bytesToString(data) )
    imagen.append( bytesToString(data) )
    imagen.pop(0)   
    
    line.set_ydata(imagen)

    return line,

def run():

    ani = FuncAnimation(
        fig, animate, init_func=init, interval=5, blit=True, save_count=10)
    plt.show()

if __name__ == "__main__":

    ser = serial.Serial("COM3", 115200)
    fig, ax = plt.subplots()
    max_x = 100
    max_rand = 1.2
    min_rand = 0
    x = np.arange(0, max_x)
    subx = np.arange(0, max_x)
    ax.set_ylim(min_rand, max_rand)
    line, = ax.plot(x, subx)
    imagen = [np.nan] * len(x)


    #py -m serial.tools.listports
    ser.write(b'2')
    run()
    ser.write(b'1')
    ser.close()
