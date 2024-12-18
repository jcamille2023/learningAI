
import cv2
import os
import sys
import subprocess
import importlib.util
import numpy as np
folder_path = os.path.join(os.getcwd(),"/opencv-video-undistorter")
print(sys.path.append(folder_path))
checkerboard_path = input("Paste ABSOLUTE path to checkerboard video.\n")
videos_path = input("Paste ABSOLUTE path to gait videos.\n") + "\\"
checkerboard_corner_x = int(input("Enter number of checkerboard corners on x axis.\n"))
checkerboard_corner_y = int(input("Enter number of checkerboard corners on y axis.\n"))


# Path to the video file

# Create a folder to store frames if it doesn't exist
output_folder = folder_path = os.path.join(os.getcwd(),"frames")
os.makedirs(output_folder, exist_ok=True)

os.makedirs(output_folder, exist_ok=True)

print("Turning checkerboard videos into frames....")
cap = cv2.VideoCapture(checkerboard_path)

# Get the frames per second (fps) of the video
fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate the frame interval to extract every 2 seconds
frame_interval = int(fps * 2)  # 2 seconds worth of frames

frame_count = 0
saved_frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()

    # Break the loop if we have reached the end of the video
    if not ret:
        break

    # Check if the current frame is at the specified interval
    if frame_count % frame_interval == 0:
        # Save the frame as an image file
        frame_path = os.path.join(output_folder, f"frame_{saved_frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        print(f"Saved {frame_path}")
        saved_frame_count += 1

    frame_count += 1

# Release the video capture object
cap.release()
print("All frames have been extracted and saved.")

print("Running camera calibration...")
i = 0
for video in os.listdir(videos_path):
    i += 1
    print("video " + str(i) + ": " + video)
    print(os.path.join(os.getcwd(),"opencv-video-undistorter/extractandcalib.py"))
    if i == 1:
        subprocess.run(["python",
                        os.path.join(os.getcwd(),"opencv-video-undistorter/extractandcalib.py"),
                        "--all",output_folder+"\\*",
                        str(checkerboard_corner_x),
                        str(checkerboard_corner_y),
                        os.path.join(output_folder+"\\","..\\undistorted_frames\\"),
                        os.path.join(videos_path, video), "undistorted_" + str(i), "False"])
        print("Calibration complete.")
    else:
        print(os.getcwd())
        subprocess.run(["./venv/Scripts/python.exe",
                        os.getcwd() + "\\opencv-video-undistorter\\extractandcalib.py",
                        "--videoprocessing",
                        videos_path + video,
                        os.path.join(output_folder+"\\","..\\undistorted_frames"),
                        "undistorted_" + str(i),
                        "False"]
                       )
i = 0
print("Getting focal lengths...")
matrix = np.loadtxt("./undistorted_frames/mtx.txt")
f_x = matrix[0,0]
f_y = matrix[1,1]
print("f_x", f_x, "f_y", f_y)
print("Running mediapipe...")
arr = os.listdir(os.path.join(videos_path,"../../undistorted_frames/"))
videos = [file for file in arr if not file.endswith(".txt")]
for video in videos:
    print("video " + str(i+1) + ": " + video)
    subprocess.run(["./venv/Scripts/python.exe","./mp.py",os.path.join(os.path.join(videos_path,"../../undistorted_frames/"), video), "undistorted_" + str(i) + ".xlsx",str(f_x),str(f_y)]);
    i += 1
print("Gait data complete!")