from ultralytics import YOLO

model = YOLO("yolov8n.pt")

result = model(source=0, show=False, conf=0.6, save=False)