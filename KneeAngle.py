import cv2
import time
import PoseModule as pm


# Capure images
cap = cv2.VideoCapture('vids\hyva.mp4')
#cap = cv2.VideoCapture(0) # for webcam capture

# Init previous time
pTime = 0

# Run model
detector = pm.poseDetector()

# Chosee side 
left = [23, 25, 27]
right = [24, 26, 28]
side = left   

while True:
    
    # Read all the images of video
    success, img = cap.read()
    
    # Find pose, landmarks and angle
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    angle = detector.findAngle(img, *side)
    
    # First frame usually can't find the landmark 
    # So check value 
    if len(lmList) != 0:
        pass

    cTime = time.time()
    fps = 1/(cTime - pTime) 
    pTime = cTime 

    # FPS Counter
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    
    # Show the images with model overlay
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    

