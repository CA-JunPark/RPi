import  serial  
import  time  # Setup serial connection  
ser = serial.Serial('/dev/ttyAMA10',  115200, timeout=0.1)  # Open serial port at 9600 baudrate 
try:  
    while True:  
        line = ser.readline().decode('utf-8') # Read a line and decode it from bytes to string  
        print('->'+str(line))  # Print the line  
        time.sleep(0.1)  
except KeyboardInterrupt:print("Program terminated!") 
ser.close()  # Close serial port