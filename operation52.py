import serial
import serial.tools.list_ports      
from multiprocessing import Process                            #Here are the libraries and modules that we used. ProcessPoolExecutor was crucial in order to Send and Receive data without problems.
import time
from concurrent.futures import ProcessPoolExecutor

def sendData(data, port, baud):                                         #This is our Send function which accepts the desired data, port, and buadrate.
    time.sleep(1)
    with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:             #time.sleep is used for suspending the execution for the given number of seconds.
        ser.reset_input_buffer()
        ser.reset_output_buffer()                                           #This flushes and resets any ouput/input that may be lingering within the serial ports.
        ser.flushInput()
        ser.flushOutput()

        data += ''                                             #The data variable is left blank for user input.
        print()
        print("Data that was sent: ", data)    
        ser.write(data.encode())                                #Any data that is sent must be encoded, otherwise it will through up an error.
        bt = time.time()                                        #Outputs the current epoch time right after sending the data in order to time our script.
        print("Current Time:", bt)                              
        
        ser.close()                                             #Closes the serial port in order to prevent any additional/unwanted data to enter.
        return bt                                               #Returns the timestamp in order to subtract it from the receive function at the end.

def receiveData(port, baud):
    time.sleep(1)
    with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:
        ser.reset_input_buffer()
        ser.reset_output_buffer()                              #The same layout that was used for the Send function can be used for the Receive function.
        ser.flushInput()
        ser.flushOutput()

        line = ser.read_until(expected=b'!END!')              #This is crucial in order to read everything that was sent in the data. 
        print()
        print("Data that was received: ", line.decode())          #Just as it was encoded, it must be decoded in order to be printed in a readable format.  
        ct = time.time()
        print("Current Time:", ct)
        
        ser.close()                                            #Same configuration is done here as from before.
        return ct

def main():

    if __name__ == "__main__":
        spObject = serial.tools.list_ports.comports()           

        serialPorts = []                                        #An empty list is created here in order to store all of the available serial ports on the system.
        print()
        for i in spObject:
            serialPorts.append(i.device)
        print('Available ports:')
        for i in range(len(serialPorts)):                                       #The ports are printed here.
            print('%i. %s' % (i+1, serialPorts[i]))
        selectedPort = int(input('Please select a port to send data to: '))      #User input is requested to select the desired serial port to send data to.
        while selectedPort-1 not in range(len(serialPorts)):
            print('Invalid input')                                                 #If the selected port is not available, it returns "Invalid Input."
            selectedPort = input('Please select a port: ')
        tty = serialPorts[selectedPort-1]                                           #Stores the selected port into a variable in order to reference it down below.
        data = input(
            'Please enter the data you want to send over the serial port: ')           #The user enters the data that they want to send.
        print()

        spObject2 = serial.tools.list_ports.comports()
        serialPorts2 = []
        for i in spObject2:
            serialPorts2.append(i.device)
        print('Available ports:')
        for i in range(len(serialPorts2)):
            print('%i. %s' % (i+1, serialPorts2[i]))                                #The same process from above is done here.
        selectedPort2 = int(input('Please select a port to listen on: '))
        while selectedPort2-1 not in range(len(serialPorts2)):
            print('Invalid input')
            selectedPort2 = input('Please select a port: ')

        lport = serialPorts2[selectedPort2-1]

        with ProcessPoolExecutor() as executor:
            p1 = executor.submit(receiveData, lport, 115200)                #This is required in order to run both functions in unison as stated above.
            p2 = executor.submit(sendData, data, tty, 115200)
            et, ft = p1.result(), p2.result()                               #The resulted timestamps are stored in the variables.

        print("Done!")
        print()                                                       #There are multiple empty print statements throughout the script in order for the output to be more pleasing to the eye, and less crowded.
        print("Elapsed Time: ", et-ft)                                #The returned variables from the functions are subtracted here in order to get an exact elasped time. The output is in seconds, but this can be easily converted to milliseconds.
        print()

main()
