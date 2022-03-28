from doctest import IGNORE_EXCEPTION_DETAIL
from logging import exception
import serial
import serial.tools.list_ports
from multiprocessing import Process #Here is the link to the documentation I referenced: https://docs.python.org/3/library/multiprocessing.html, Drew

def sendData(data, port, baud):
    ser = serial.Serial(port, baud)    
   
    try:
        ser.isOpen()
    except Exception:
            pass
       
    data += "\r\n"
    ser.write(data.encode()) 

def receiveData(port, baud): 
    ser = serial.Serial(port, baud) 

    ser.timeout = 0
    line = ser.readline()
    print(line.decode())
    
def main():
    if __name__ == "__main__":
        spObject = serial.tools.list_ports.comports()
        serialPorts = []
        for i in spObject:
            serialPorts.append(i.device)
        print('Available serial ports:')
        for i in range(len(serialPorts)):
            print('%i. %s' %(i+1,serialPorts[i])) 
        selectedPort = int(input('Please select a port: '))
        while selectedPort-1 not in range(len(serialPorts)):
            print('Invalid input')
            selectedPort = input('Please select a port: ')
        tty = serialPorts[selectedPort-1] 
        data = input('Please enter the data you want to send over the serial port: ')
        
        spObject2 = serial.tools.list_ports.comports()
        serialPorts2 = []
        for i in spObject2:
            serialPorts2.append(i.device)
        print('Available serial ports:')
        for i in range(len(serialPorts2)):
            print('%i. %s' %(i+1,serialPorts2[i])) 
        selectedPort2 = int(input('Please select a port: '))
        while selectedPort2-1 not in range(len(serialPorts2)):
            print('Invalid input')
            selectedPort2 = input('Please select a port: ')
        
        lport = serialPorts2[selectedPort2-1]
        
        p1 = Process(target=sendData(data, tty, 115200))
        p2 = Process(target=receiveData(lport, 115200))
        
        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
        print("Done!")

main()
