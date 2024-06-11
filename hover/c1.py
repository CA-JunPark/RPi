import serial
import struct
import time
import ctypes


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
ser = serial.Serial('/dev/ttyAMA0', HOVER_SERIAL_BAUD, timeout=0.1)

# ########################## STRUCTS ##########################
SerialCommand = struct.Struct('<HhhH')  # Start, Steer, Speed, Checksum
# Start, Cmd1, Cmd2, SpeedR, SpeedL, WheelR, WheelL, BatVoltage, BoardTemp, CmdLed, Checksum
SerialFeedback = struct.Struct('<HhhhhhhhhHH')



# ########################## SEND ##########################sAS
def Send(uSteer, uSpeed):
    global steer
    START = ctypes.c_uint16(START_FRAME).value
    STEER = uSteer
    SPEED = uSpeed
    checksum = ctypes.c_uint16(START ^ STEER ^ SPEED).value
    print(START, STEER, SPEED, checksum)
    try:
        print(SerialCommand.pack(START, STEER, SPEED, checksum))
    except Exception as e:
        print(e)
    ser.write(SerialCommand.pack(START, STEER, SPEED, checksum))

# ########################## RECEIVE ##########################
def Receive():
    # Read data from the serial port
    data = ser.read(SerialFeedback.size)

    if len(data) == SerialFeedback.size:
        feedback = SerialFeedback.unpack(data)

        # Check validity of the new data
        start, cmd1, cmd2, speedR_meas, speedL_meas, wheelR_cnt, wheelL_cnt, batVoltage, boardTemp, cmdLed, checksum = feedback
        if start == START_FRAME and checksum == (start ^ cmd1 ^ cmd2 ^ speedR_meas ^ speedL_meas ^ wheelR_cnt ^ wheelL_cnt ^ batVoltage ^ boardTemp ^ cmdLed):
            # Print data
            print(f"1: {cmd1} 2: {cmd2} 3: {speedR_meas} 4: {speedL_meas} r: {wheelR_cnt} l: {wheelL_cnt} 5: {batVoltage} 6: {boardTemp} 7: {cmdLed}")
        else:
            print(f"1: {cmd1} 2: {cmd2} 3: {speedR_meas} 4: {speedL_meas} r: {wheelR_cnt} l: {wheelL_cnt} 5: {batVoltage} 6: {boardTemp} 7: {cmdLed}")
            print("Non-valid data skipped")

#======================= Main ========================
if __name__ == "__main__":
    while True:
        try:
            Send(0, 100)
            time.sleep(TIME_SEND)
        except:
            break
