from doctest import IGNORE_EXCEPTION_DETAIL
from logging import exception
import serial
import serial.tools.list_ports      
from multiprocessing import Process
import time
from datetime import datetime
import threading
#Test different way of handling processes
from concurrent.futures import ProcessPoolExecutor

class Timer:

    def sendData(data, port, baud, self):
        time.sleep(1)
        with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:   
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.flushInput()
            ser.flushOutput()

            data += ''
            print()
            print("Data that was sent: ", data)    
            ser.write(data.encode())
            bt = time.time()
            self._start_time = time.perf_cunter()
            print("Current Time:", bt)
            
            ser.close()

    def receiveData(port, baud, self):

        time.sleep(1)
        with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()               
            ser.flushInput()
            ser.flushOutput()

            line = ser.read_until(expected=b'!END!')
            print()
            print("Data that was received")             
            print(line.decode())
            ct = time.time()
            print("Current Time:", ct)
            elasped_time = time.perf_counter() - self._start_time
            print("Elasped Time: ", elasped_time)
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

            with ProcessPoolExecutor() as executor:
                p1 = executor.submit(receiveData, lport, 115200)
                p2 = executor.submit(sendData, data, tty, 115200)

            print("Done!")
            print()
main()
