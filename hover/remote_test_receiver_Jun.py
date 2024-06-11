import serial
import struct
import time
# from pynput.keyboard import Key, Listener, KeyCode
import ctypes
import socket

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
SPEED_MAX_TEST = 100            # [-] Maximum speed for testing
CURRENT_SPEED = 0               # [-] Current speed for testing
# DEBUG_RX = True               # [-] Debug received data. Prints all bytes to serial (comment-out to disable)

# ########################## SERIAL SETUP ##########################
# Replace '/dev/ttyUSB0' with the appropriate serial port for your Raspberry Pi
ser = serial.Serial('/dev/ttyAMA10', HOVER_SERIAL_BAUD, timeout=0.1)
# ########################## STRUCTS ##########################
SerialCommand = struct.Struct('<HhhH')  # Start, Steer, Speed, Checksum
# Start, Cmd1, Cmd2, SpeedR, SpeedL, WheelR, WheelL, BatVoltage, BoardTemp, CmdLed, Checksum
SerialFeedback = struct.Struct('<HhhhhhhhhHH')


# ########################## SEND ##########################sAS
def Send(uSteer, uSpeed):
    # Create command
    START = ctypes.c_uint16(START_FRAME).value
    STEER = uSteer
    SPEED = uSpeed
    checksum = ctypes.c_uint16(START ^ STEER ^ SPEED).value
    # Write to Serial
    ser.write(SerialCommand.pack(START, STEER, SPEED, checksum))

# ########################## LOOP ##########################
import threading
speed = 0
steer = 0
jump = 4
SPEED_MAX = 50


def getInput(key):
    global speed, steer

    if key == 'w':
        speed += jump
    elif key == 's':
        speed -= jump

    elif key == 'a':
        if speed != 0: # Steering should not happend when the speed = 0
            steer -= jump
    elif key == 'd':
        if speed != 0: # Steering should not happend when the speed = 0
            steer += jump


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
   
    # Speed and Steer command
    t = threading.Thread(target=sending, args=())
    t.start()

    # listener
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                if abs(speed) < SPEED_MAX:
                    if speed > 0:
                        speed -= jump
                    elif speed < 10:
                        speed += jump

                if steer > 0:
                    steer -= jump
                elif steer < 0: 
                    steer += jump
            else:
                getInput(data)
            print("->" + str(data))
            print(f"Steer:{steer}, Speed:{speed}")
        except:
            conn.close()
            t.join()
            break
       
            