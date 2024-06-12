# from picamera2 import Picamera2, Preview
# import time
# picam2 = Picamera2()
# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)
# # time.sleep(2)
# # picam2.capture_file("test.jpg")
# # picam2.close()
import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)

picam2.start()
while 1:
    time.sleep(1)
