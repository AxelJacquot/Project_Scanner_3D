import serial
from serial.tools.list_ports import comports

def ask_for_port():
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        if desc == "FT232R USB UART":
            return port
    return 0
def ports():
    n = 0
    while n < 5:
        port = ask_for_port()
        if port == 0: 
            n = n + 1
            print("Veuillez brancher l'UART de la STM32")
            raw_input("Appuyer sur entree pour refaire une verification")
        else:
            return port
    print("FERMETURE DU PROGRAMME")

ser = serial.Serial()
ser.baudrate = 115200
ser.port = ports()
ser.open()
out = 0
while 1:
    data = input("Valeur a envoye: ")
    ser.write([data])
    if data == 56:
        out = ser.readline()
        print(out)