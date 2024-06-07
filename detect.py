import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from gpiozero import LED
from time import sleep
LED_B = LED(13)
LED_R = LED(21)
LED_G = LED(19)
LED_B.on()
# Initialize the Picamera2
picam2 = Picamera2()
# picam2.preview_configuration.main.size = (1080, 720)
picam2.preview_configuration.main.format = "RGB888"
# picam2.preview_configuration.align()
# picam2.configure("preview")
picam2.start()

# Load the YOLOv8 model
model = YOLO("/home/airobot/yolov8/best.pt")

LED_R.on()
while True:
    frame = picam2.capture_array()
    results = model(frame)
    #annotated_frame = results[0].plot()
    for r in results:  
        boxes = r.boxes
        for box in boxes:        
            c = box.cls
            name = str(model.names[int(c)])
            if "Button" in name:
                LED_G.on()
    #cv2.imshow("Camera", annotated_frame)
    sleep(1)
    LED_G.off()

    # Break the loop if 'q' is pressed
    # if cv2.waitKey(1) == ord("q"):
    #     break

# cv2.destroyAllWindows()