import serial
import time

ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyUSB0'
ser.open()

while 1:
    ser.write(51)
    time.sleep(2)