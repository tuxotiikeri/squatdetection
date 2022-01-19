import csv
from json import detect_encoding
import numpy as np
import cv2
import time
import PoseModule as pm

# Capure images
cap = cv2.VideoCapture('vids\hyva5.mp4')
#cap = cv2.VideoCapture(0) # for webcam capture

# Init previous time
pTime = 0

# Init Max Distance between leg and hip
maxDistance = 100

# Init counter
count = 0

# Init Direction 
dir = 0

'''Squat depth ratio
   Euclidean distance between hip and ankle landmarks 
   0.75 for shallow squat (knee flexion around 90 deg)
   0.5 for pistol squat (all the way down)'''
depth = 0.5
     
# Run model
detector = pm.poseDetector()

# Chosee side 
left = [23, 25, 27]
right = [24, 26, 28]
side = right

while True:
        
        # Read all the images of video
        success, img = cap.read()
        
        # Find pose, landmarks, angle and distance
        img = detector.findPose(img, draw=False)
        lmList = detector.findPosition(img, draw=False)
        angle = detector.findAngle(img, *side)
        distance = detector.findDistance(img, side[0], side[2])
        
                
        # First frame usually can't find the landmark 
        # So check value 
        if len(lmList) != 0:
            
            # Calc distance between lm 1 and 3
            # trying to find max distance between ankle and hip
            # and using that as a straight leg measurement
            if distance > maxDistance:
                maxDistance = distance
            per  = np.interp(distance, (maxDistance * depth, maxDistance * .96), (0, 100))

            # Range of motion
            bar = np.interp(distance, (maxDistance * depth, maxDistance * .96), (650, 100))

            # Going up
            color = (135, 135, 135) # gray bar
            if per == 100:
                color = (0, 255, 0) # green bar
                if dir == 1:
                    count += 0.5 
                    dir = 0
                    
            # Going down
            if per == 0:
                color = (0, 255, 0) # green bar
                if dir == 0: 
                    count += 0.5 # adding 0.5 reps to counter when position low enough
                    dir = 1
            
            # Draw rep progression bar
            cv2.rectangle(img, (1100, 100), (1170, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1170, 650), (135, 135, 135), cv2.FILLED) # showing reps as integer, so the half reps are not visible to user
            cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)
                
            # Draw rep counter
            cv2.rectangle(img, (0, 550), (150, 720), (135, 135, 135), cv2.FILLED)
            cv2.putText(img, str(int(count)), (30, 690), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 5)
    

        # FPS counter (left upper corner)
        cTime = time.time()
        fps = 1/(cTime - pTime) 
        pTime = cTime 
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        
        # Show the images with model overlay
        cv2.imshow("Image", img)
        cv2.waitKey(1)
