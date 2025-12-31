import os
from ultralytics import YOLO
import cv2
import csv

video_path = 'video_15000.mp4'
video_name = video_path.split('.')[0]
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H,W, _ = frame.shape
model_path = 'runs-20231001T064404Z-001/runs/detect/train/weights/best.pt'
model = YOLO(model_path)
threshold = 0.5
c=0

csv_file_path = f'{video_name}.csv'
header = ["frames", "x1", "y1", "x2", "y2", "class"]
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

while ret:
    results = model(frame)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            data_to_append = [f"frame{c}", int(x1), int(y1), int(x2), int(y2), results.names[int(class_id)].lower()]
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data_to_append)

    c=c+1
    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()