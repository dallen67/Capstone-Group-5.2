from doctest import IGNORE_EXCEPTION_DETAIL
from logging import exception
import serial
import serial.tools.list_ports      
               #All of these modules are required for the script to run. We also needed multiprocessing in order to run all of the functions at once.
from multiprocessing import Process
import time
from datetime import datetime


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
        ser.reset_input_buffer()    #these four lines ensure that the receiving port is clear of any previous data
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
        spObject = serial.tools.list_ports.comports()          #This function will return all the serial ports on the system, but it returns them as an object

        serialPorts = []                  #This is an empty list to store the serial port names
        print()
        for i in spObject:
            serialPorts.append(i.device)    #every serial port name that is found on the system will be added to the serialPorts list from above.
        print('Available ports:')           #this prints all available ports
        for i in range(len(serialPorts)):
            print('%i. %s' % (i+1, serialPorts[i]))
        selectedPort = int(input('Please select a port to send data to: '))      #this asks for user input to select the designated port to send data to for the send function.
        while selectedPort-1 not in range(len(serialPorts)):
            print('Invalid input')
            selectedPort = input('Please select a port: ')
        tty = serialPorts[selectedPort-1]
        data = input(
            'Please enter the data you want to send over the serial port: ')
        print()

        spObject2 = serial.tools.list_ports.comports()          #this asks for user input to select the designated port to send data to for the receive function.
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

        p1 = Process(target=sendData(data, tty, 115200)) #here we start the multiprocessing
        p2 = Process(target=receiveData(lport, 115200))

        p2.start()
        
        print("Start", datetime.now())
        ans = str()
        while ans != 'end': 
            ans = input()
            ans = ans.lower()
        print("End", datetime.now())
        
        p1.start()

        p2.join()
        p1.join()
        print("Done!") #finally we use this print statement to confirm that the code finished executing successfully
        print()


main()
