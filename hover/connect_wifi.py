import os

def connect(ssid, password):
    command = f"nmcli dev wifi connect '{ssid}' password '{password}'"
    result = os.system(command)
    if result == 0:
        print(f"connected to {ssid}")
    else:
        print("failed to connect to wifi")

ssid = "TWUGuest"
password = ""
connect(ssid, password)