import cv2
import os

# Video file path
video_path = 'example_5_out.mp4'

# Directory to save PNG frames
output_folder = 'frames3/'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Initialize a frame counter
frame_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop when all frames have been processed

    # Save the frame as a PNG image in the output folder
    frame_filename = os.path.join(output_folder, f'frame_{frame_counter:03d}.png')
    cv2.imwrite(frame_filename, frame)

    frame_counter += 1

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()

print(f'Saved {frame_counter} frames in {output_folder}')
