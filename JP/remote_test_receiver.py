import socket
import serial
import struct
import time
import ctypes
from gpiozero import LED
ledb = LED(17)
ledg = LED(12)
ledr = LED(16)

time.sleep(20)


# ########################## WiFi ##########################
import os
def connect(ssid, password):
    command = f"nmcli dev wifi connect '{ssid}' password '{password}'"
    result = os.system(command)
    if result == 0:
        print(f"connected to {ssid}")
        ledg.on()
    else:
        print("failed to connect to wifi")
        ledr.on()

ssid = "TWUGuest"
password = ""
print("connecting to wifi")
connect(ssid, password)

# ########################## DEFINES ##########################
# [-] Baud rate for HoverSerial (used to communicate with the hoverboard)
HOVER_SERIAL_BAUD = 115200
# [-] Start frame definition for reliable serial communication
START_FRAME = 0xABCD
TIME_SEND = 0.1                 # [s] Sending time interval
SPEED_MAX_TEST = 70            # [-] Maximum speed for testing
CURRENT_SPEED = 0               # [-] Current speed for testing
# DEBUG_RX = True               # [-] Debug received data. Prints all bytes to serial (comment-out to disable)
# ########################## SERIAL SETUP ##########################
# Replace '/dev/ttyUSB0' with the appropriate serial port for your Raspberry Pi
ser = serial.Serial('/dev/ttyAMA0', HOVER_SERIAL_BAUD, timeout=0.1)
# ########################## STRUCTS ##########################
SerialCommand = struct.Struct('<HhhH')  # Start, Steer, Speed, Checksum
# Start, Cmd1, Cmd2, SpeedR, SpeedL, WheelR, WheelL, BatVoltage, BoardTemp, CmdLed, Checksum
SerialFeedback = struct.Struct('<HhhhhhhhhHH')


speed = 0
steer = 0
# ########################## SEND ##########################sAS
def Send(Steer, Speed):
    global speed, steer
    START = ctypes.c_uint16(START_FRAME).value
    STEER = Steer-1 #to make the car go straight
    SPEED = Speed
    checksum = ctypes.c_uint16(START ^ STEER ^ SPEED).value
    ser.write(SerialCommand.pack(START, STEER, SPEED, checksum))

def accelerate(Target, Rate): #accelerate(Target Speed, Rate of change)
    global speed, steer

    if Target > SPEED_MAX_TEST:
        Target = SPEED_MAX_TEST
    # calculate the speed jump
    change = abs(Target - speed)
    # if the rate of change is too big, set it to default 10 per 0.1 seconds
    if Rate > change:
        Rate = 10

    # to increase the speed or decrease the speed gradually
    if Target > speed:
        for i in range (change//Rate):
            speed += Rate
            Send(steer, speed)
            time.sleep(TIME_SEND)
        for i in range (change%Rate):
            speed += 1
            Send(steer, speed)
            time.sleep(TIME_SEND) 
    if Target < speed:
        for i in range (change//Rate):
            speed -= Rate
            Send(steer, speed)
            time.sleep(TIME_SEND)
        for i in range (change%Rate):
            speed -= 1
            Send(steer, speed)
            time.sleep(TIME_SEND)    

    print(f"Steer:{steer}, Speed:{speed}")


def stop():
    global steer, speed
    accelerate(0, 30)
    steer = 0

def turn_left():
    global steer, speed
    tmp = speed
    for _ in range(80-tmp):
        Send(-(speed//2)-5, speed+5)
        time.sleep(TIME_SEND)      
    steer = 0
    

def turn_right():
    global steer, speed
    tmp = speed
    for _ in range(80-tmp):
        Send((speed//2)+5, speed-5)
        time.sleep(TIME_SEND)      
    steer = 0

#======================= Main ========================
import threading

def sending():
    while True:
        try:
            Send(steer, speed)
            time.sleep(TIME_SEND)
        except:
            break

if __name__ == "__main__":
    #Connect to WiFi and listen to remote commands
    host = '10.18.11.88'
    port = 5000
    server_socket = socket.socket() 
    server_socket.bind((host, port)) 
    server_socket.listen(1)
    print('Waiting for connection...')
    conn, address = server_socket.accept()
    print("connected from: " + str(address) + "\n")
    ledb.on()
    t = threading.Thread(target=sending, args=())
    t.start()
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data ==  "w":
                speed+=10
            elif data ==  "s":
                speed-=10

            elif data ==  "a":
                turn_left()
            elif data ==  "d":
                turn_right()

            elif data == "p":
                stop()

            print("->" + str(data))
            accelerate(speed, 10)
        except:
            conn.close()
            t.join()
            break