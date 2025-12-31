import os
import torch

from ultralytics import YOLO
import cv2




video_path = 'example_5.mp4'
video_name = video_path.split('.')[0].split('/')[-1]
video_path_out = f'{video_name}_out.mp4'

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = 'runs/detect/train3/weights/best.pt'

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5

while ret:

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            # Draw the bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)

            # Calculate the center of the bounding box
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Add a red dot at the center
            cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), -1)

            # Add the class name as text
            #cv2.putText(frame, results.names[int(class_id)].lower(), (int(x1), int(y1 - 10)),
                        #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()



cap.release()
out.release()
cv2.destroyAllWindows()