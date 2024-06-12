import  serial  
import  time  # Setup serial connection  
ser = serial.Serial('/dev/ttyAMA0',  115200, timeout=0.1)  # Open serial port at 9600 baudrate 


while True:
    try:
        ser.write(b'Hello, world!\n')
        response = ser.readline()
        print("Received:", response.decode('utf-8'))
        time.sleep(1)
    except:
        ser.close()
