import serial
#from datetime import datetime


if __name__ == "__main__":

	ser = serial.Serial("COM3", 115200)
	ser.write(b'2')#La b significa byte. ascci caracter representacion de un unico caracter.

	data = []
	for i in range(100):
		if i % 4 == 0 and i != 0:
			#print( ''.join([chr(k) for k in data]) )
			#print( ''.join(data).decode('utf-8') )
			value = ''.join([k.decode('utf-8') for k in data]) #type string
			print( value )
			data = []
		data.append(ser.read())

		


	ser.write(b'1')
	ser.close()

	