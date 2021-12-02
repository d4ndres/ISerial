import serial
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


ser = serial.Serial("COM3", 115200)


fig, ax = plt.subplots()

max_x = 100#ramaño de muestras
max_rand = 5#valor imagen max
min_rand = 0#valor imagen min

x = np.arange(0, max_x)
subx = np.arange(0, max_x)
ax.set_ylim(min_rand, max_rand)

line, = ax.plot(x, subx)#Los parametros son dos listas con el mismo tamaño. representa el eje x

imagen = [np.nan] * len(x)

def bytesToString(listOfBytes):
	return float(''.join([k.decode('utf-8') for k in listOfBytes]))


def init():  # give a clean slate to start
    line.set_ydata( imagen )
    return line,


def animate(frame):  # update the y values (every 1000ms)

    data = []
    for i in range(4):
    	data.append(ser.read())
    imagen.append( bytesToString(data) )
    imagen.pop(0)	
  
    line.set_ydata(imagen)

    return line,

def run():
	ani = FuncAnimation(
	    fig, animate, init_func=init, interval=5, blit=True, save_count=10)

	plt.show()

if __name__ == "__main__":
	#py -m serial.tools.listports
	ser.write(b'2')
	run()
	ser.write(b'1')
	ser.close()
