import serial
from matplotlib import pyplot as plt


if __name__ == "__main__":

	with serial.Serial("COM3", 115200) as ser:	
		ser.write(b'2')
		data = []
		y = []
		i = 0
	
		try: 
			while True:
				if i % 4 == 0 and i != 0:
					value = ''.join([k.decode('utf-8') for k in data]) #type string
					print( value )
					y.append( float(value) )
					data = []
				data.append(ser.read())
				i += 1
		except KeyboardInterrupt:
			ser.write(b'1')
			print("KeyboardInterrupt")
			print(y)
			plt.plot( y )
			#plt.axis([-1, len(y) + 1, -(min(y)+0.01)/10, max(y) + max(y)/100])#Inecesario
			plt.show()
