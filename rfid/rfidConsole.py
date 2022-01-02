import serial
import getch
import sys
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

clearConsole()

if len(sys.argv) < 2:
    print ("Missing COM port argument, usage example:\npython3 rfid_read.py COM9\n\nExiting")
    quit()
else:
    port = str(sys.argv[1])

try:
    ser = serial.Serial(port, 2400, timeout = 1)  # open serial port
except:
    print ("Error: Cannot open port {}\nExiting".format(port))
    quit()

scan = True
print_char = ['|', '/', '-', '\\']
try:
    while (scan):
        data  = '0'
        print ("******** RFID READER ********")
        print ("Place an RFID card on scanner")
        ser.setDTR(True)
        data='0'
        for i in range(0,5):
            print ("-- Searching for cards  {}  --\033[A".format(print_char[i%4]))
            data = ser.read(12)
            if len(data)==12:
                break
        ser.setDTR(False)
        ser.flushInput()
        if len(data) == 12:
            print ("\n ----------------------------\n| SUCCESS, RFID = {} |\n ----------------------------".
                format(data[1:10].decode('utf-8')))
            print ("Press any key to scan another card or q/Q to quit")
            if getch.getch() == ('q' or 'Q'):
                scan = False
        else:
            print ("\nNo card detected, press any key to try again or q/Q to quit")
            if (getch.getch() == ('q' or 'Q')):
                scan = False
        clearConsole()
    ser.close()
    print ("RFID Scanner finished")
except:
    ser.close()

