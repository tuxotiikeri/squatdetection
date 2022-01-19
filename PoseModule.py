from json import detect_encoding
import numpy as np
import cv2
import mediapipe as mp
import time
import math

class poseDetector():
 
    def __init__(self, mode=False, modelComplex=1, segmentation=False,
                 smooth=True, detectionCon=0.5, trackCon=0.5):
        
        # Init class parameters 
        self.mode = mode
        self.modelComplex = modelComplex
        self.segmentation = segmentation
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.modelComplex, self.segmentation,
                                     self.smooth, self.detectionCon, self.trackCon)

    # Model display settings
    def findPose(self, img, draw = True):
        ''' find pose and return img
            the landmards and connecting segments are drawn 
            if landmarks are detected'''
                   
        # Convert color space
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get detection
        self.results = self.pose.process(imgRGB)

        # Check landmark detection
        if self.results.pose_landmarks:
            
            # Check draw parameter
            if draw:
                
                # Draw landmarks and the connections between
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                        self.mpPose.POSE_CONNECTIONS)

        return img
    
    def findPosition(self, img, draw = True):
        '''
            The landmarks are written as point in image in range 0-1
            so the we need to get the image shape.
            Relative values need to be divided with image shape to get the 
            actual pixel values (as integers)
        '''

        # Init landmark list
        self.lmList = []
        
        # If results are available
        if self.results.pose_landmarks:
            
            # Get landmarks as list    
            for id, lm in enumerate(self.results.pose_landmarks.landmark):

                h, w, c, = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                
                if draw:               
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        
        return self.lmList
     
    def findAngle(self, img, p1, p2, p3, draw=True):
        
        '''Calculates angle between three landmarks
           returns angle as float
           Overlays True / False
        '''
    
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the angle betweeen point 1 ,2 and 3
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            
            if 170 <= angle <= 190:
                
                # Angle OK
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
                cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), 2)
                cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), 2)
                cv2.circle(img, (x3, y3), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 255, 0), 2)
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                
            else:
                
                # Angle out of range
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
                cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
                cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                
        return angle
        
        
    def findDistance(self, img, p1, p3, draw=False):
            
        '''Calculates distance between two points (first and third landmark)
            returns distance as float
            Overlays True / False
        '''

        # Get the landmarks 1 and 3
        x1, y1 = self.lmList[p1][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the distance between two lines
        d = ((x1 - x3)**2 + (y1 - y3)**2)**0.5
                    
        return d
     
def main():
    
        
    # Capure images
    cap = cv2.VideoCapture('vids\hyva.mp4') # pistol outside
    #cap = cv2.VideoCapture(0) # for webcam capture
    
    # Init previous time
    pTime = 0
    
    # Choose landmarks for left or right side
    left = [23, 25, 27]
    right = [24, 26, 28]
    side = left
    
    # Run model
    detector = poseDetector()
    
    while True:
        
            # Read all the images of video
            success, img = cap.read()
            
            # Find pose, landmarks and angle
            img = detector.findPose(img, draw=True)
            lmList = detector.findPosition(img, draw=False)
            
            # First frame usually can't find the landmark 
            # So check value 
            if len(lmList) != 0:
                    pass
            
            # Show the images with model overlay
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        

if __name__ == "__main__":
     main()