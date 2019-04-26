import serial
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyUSB0'
ser.open()
out = 0
while 1:
    data = input("Valeur a envoye: ")
    ser.write([data])
    if data == 56:
        out = ser.readline()
        print(out)