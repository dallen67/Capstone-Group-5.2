from doctest import IGNORE_EXCEPTION_DETAIL
from logging import exception
import serial
import serial.tools.list_ports      
               #All of these modules are required for the script to run. We also needed multiprocessing in order to run all of the functions at once.
from multiprocessing import Process
import time


def sendData(data, port, baud):     #the send data function receives the data, port, and baud (automatically assigned) from the user input below.
    time.sleep(1)                   #suspends execution for the given number of seconds
    with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:   
        ser.reset_input_buffer()   #resets any input/output buffer that might still be lingering in order to avoid any potential errors and such.
        ser.reset_output_buffer()
        ser.flushInput()
        ser.flushOutput()
        
        data += ''
        print()                               #there are various empty print statements in the script, so that the user input and such looks more organzied and not so crammed.
        print("Data that was sent: ", data)    #we left this here for confirmation of what was sent.
        ser.write(data.encode())                #pySerial requires on Python 3 that all data that is sent must be encoded. It will not let you send any data with encoding.
        ser.close()                             #closes the port immediately after everything is sent.


def receiveData(port, baud):
    time.sleep(1)
    with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:
        ser.reset_input_buffer()
        ser.reset_output_buffer()               
        ser.flushInput()
        ser.flushOutput()
        
        line = ser.read_until(expected=b'!END!')
        print()
        print("Data that was received")             #the receive function is very similiar to the send function.
        print(line.decode())
        ser.close()


def main():

    if __name__ == "__main__":
        spObject = serial.tools.list_ports.comports()
        serialPorts = []
        print()
        for i in spObject:
            serialPorts.append(i.device)
        print('Available ports:')
        for i in range(len(serialPorts)):
            print('%i. %s' % (i+1, serialPorts[i]))
        selectedPort = int(input('Please select a port to send data to: '))
        while selectedPort-1 not in range(len(serialPorts)):
            print('Invalid input')
            selectedPort = input('Please select a port: ')
        tty = serialPorts[selectedPort-1]
        data = input(
            'Please enter the data you want to send over the serial port: ')
        print()

        spObject2 = serial.tools.list_ports.comports()
        serialPorts2 = []
        for i in spObject2:
            serialPorts2.append(i.device)
        print('Available ports:')
        for i in range(len(serialPorts2)):
            print('%i. %s' % (i+1, serialPorts2[i]))
        selectedPort2 = int(input('Please select a port to listen on: '))
        while selectedPort2-1 not in range(len(serialPorts2)):
            print('Invalid input')
            selectedPort2 = input('Please select a port: ')

        lport = serialPorts2[selectedPort2-1]

        p1 = Process(target=sendData(data, tty, 115200))
        p2 = Process(target=receiveData(lport, 115200))

        p2.start()
        p1.start()

        p2.join()
        p1.join()
        print("Done!")
        print()


main()
