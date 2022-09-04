#!/usr/bin/env python3

# To see CV debug information, do
#
#    OPENCV_VIDEOIO_DEBUG=1 debug/test-camera.py

# Python program to save a video using OpenCV and output FPS
#
# from https://www.geeksforgeeks.org/saving-a-video-using-opencv/
import os
import sys
import time

import cv2


video_channel = 0
if len(sys.argv) > 1:
    video_channel = int(sys.argv[1])

# Create an object to read
# from camera
video = cv2.VideoCapture(video_channel)

# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (frame_width, frame_height)

print(f"starting video_channel={video_channel} size={size}", )

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
writer = cv2.VideoWriter('camera_test_output.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

print("recording 30 secs of video...")
start = time.time()
num_frames = 0
while(True):
    ret, frame = video.read()

    if ret == True:
        # Write the frame into the
        # file 'filename.avi'
        writer.write(frame)
        num_frames += 1

    # Break the loop
    else:
        break

    # runs for 30s
    if time.time() - start >= 30:
        break

# When everything done, release
# the video capture and video
# write objects
video.release()
writer.release()


print("The video was successfully saved.")
print(f"recorded {num_frames} frames in 30s ({num_frames/30:.2f} fps)")
print("")
print("You can view the video recorded with:")
print("   scp pi@raspberrypi.local:/home/pi/scatbot-ai-shootout/camera_test_output.avi . && open camera_test_output.avi")
print("on your local machine")
