from doctest import IGNORE_EXCEPTION_DETAIL
from logging import exception
import serial
import serial.tools.list_ports      
from multiprocessing import Process
import time
import rsa
from concurrent.futures import ProcessPoolExecutor

def sendData(data3, port, baud):     
    time.sleep(1)                   
    with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:   
        ser.reset_input_buffer()  
        ser.reset_output_buffer()
        ser.flushInput()
        ser.flushOutput()
        
        data3 += '/n'
        print()                              
        print("Data that was sent: ", data3)    
        ser.write(data3)               
        ser.close()                             


def receiveData(port, baud):
  
    time.sleep(1)
    with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:
        ser.reset_input_buffer()    
        ser.reset_output_buffer()               
        ser.flushInput()
        ser.flushOutput()
        
        privateKey = rsa.newkeys(512)
        line = ser.read_until(expected=b'!END!')
        line2 = line.decode()
        line3 = rsa.decrypt(line2, privateKey)
        
        print()
        print("Data that was received")            
        print(line3)
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
        
        publicKey = rsa.newkeys(512)
        
        data = input('Please enter the data you want to send over the serial port: ')
        data2 = data.encode()
        
        data3 = rsa.encrypt(data2, publicKey)
        
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


        with ProcessPoolExecutor() as executor:
            p1 = executor.submit(receiveData, lport, 115200)
            p2 = executor.submit(sendData, data, tty, 115200)
        print("Done!") 
        print()


main()
