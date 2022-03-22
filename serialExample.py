import serial # This is the module that provides serial support, it needs to be install with pip
import serial.tools.list_ports # This is a tool to list ports

def sendData(data, port, baud): # Start reading at the next function, not this one
    ser = serial.Serial(port, baud) # creates a serial object using the port name and speed provided, this is where serial data is sent
    data += "\r\n" ## Serial is very old and just sends a stream of characters. 
    # This is the default end of line character for serial and is a carryover from when computer displays were typewriters
    # \r is a carriage return which moves the typewriter back to the beginning of the line
    # \n is a line feed which moves the page up to a new line
    # Windows still uses \r\n as a line terminator but most other platforms just use \n
    # Serial can use either but defaults to /r/n
    ser.write(data.encode()) # This writes the data to the port, it must be encodes as bytes before it can be sent over serial

def receiveData: #my attempt to write a receive function for the program, Drew Allen
    ser = serial.Serial()
    ser.port = ""
    ser.baudrate = 115200
    ser.timeout = 0
    line = ser.readline()
    print(line)


def main():
    spObject = serial.tools.list_ports.comports() # This function will return all the serial ports on the system, but it returns them as an object
    serialPorts = [] # This is a list to store the serial port names
    for i in spObject: # This loop runs through all the serial ports in the serial ports object
        serialPorts.append(i.device) # This adds the device name to the list of port names
    print('Available serial ports:')
    for i in range(len(serialPorts)): # The len() function returns the number of items in the list. 
        # A for loop in Python is only able to iterate a list, not a number.
        # The range() function will create a list starting at zero up to the number before the number entered
        # For example, range(5) will return the list [0,1,2,3,4]
        print('%i. %s' %(i+1,serialPorts[i])) # This is a formatted print. It's a cleaner way to insert variables into a print statement. 
        #I used i+1 because starting at 1 is more natural for a human-interactive list and Python indexes start at 0
    selectedPort = int(input('Please select a port: ')) # The input() function returns a string but I want a number.
    # The int() functions casts the string into an integer
    while selectedPort-1 not in range(len(serialPorts)): # If the number entered was not in the list of available port.
        #It will continue to prompt the user until they enter a valid option
        print('Invalid input')
        selectedPort = input('Please select a port: ')
    tty = serialPorts[selectedPort-1] # The input we got from the user was just the number on the list. 
    #This just gets the port name from the position selected on the list
    data = input('Please enter the data you want to send over the serial port: ') # This just gets a string of data from the user to send over the serial port

    sendData(data, tty, 115200) # Calls the send function and passes the data the user wants to send, the port they want to use, and the speed

    # I didn't provide any confirmation of success here. You'll want to listen on the other end of the serial cable to make sure your data goes through.

    receiveData()

main()
