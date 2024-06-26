import serial
import struct
import time
import ctypes
from gpiozero import LED
ledb = LED(17)
ledg = LED(12)
ledr = LED(16)

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



speed = 0
steer = 0
# ########################## SEND ##########################sAS
def Send(Steer, Speed):
    global speed, steer
    START = ctypes.c_uint16(START_FRAME).value
    STEER = Steer-2
    SPEED = Speed
    checksum = ctypes.c_uint16(START ^ STEER ^ SPEED).value
    ser.write(SerialCommand.pack(START, STEER, SPEED, checksum))

def accelerate(Target, Rate): #accelerate(Target Speed, Rate of change)
    global speed, steer
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
    accelerate(0, 10)

#======================= Main ========================
if __name__ == "__main__":

    ledr.on()
    time.sleep(1)
    ledr.off()

    ledb.on()
    time.sleep(1)
    ledb.off()

    ledg.on()
    time.sleep(1)
    ledg.off()

    for _ in range(50):
        Send(0, 50)
        time.sleep(TIME_SEND)

    for _ in range(60):
        Send(-35, 65)
        time.sleep(TIME_SEND)

    for _ in range(50):
        Send(0, 50)
        time.sleep(TIME_SEND)

    for _ in range(60):
        Send(35, 25)
        time.sleep(TIME_SEND)

    for _ in range(50):
        Send(0, 50)
        time.sleep(TIME_SEND)
    
    stop()
