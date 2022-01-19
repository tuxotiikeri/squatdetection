# squatdetection

Squat detection for testing blazepose model for single leg squats. 

**PoseModule.py** is main module and has all the functions for detecting landmarks and for calculating angles and distances.

On default running the **PoseModule.py** will draw full BlazePose model (33 landmarks) over the image.

![image](https://user-images.githubusercontent.com/11043247/150089845-5ce1cd7f-7f2c-442f-8d1c-ebbd121406e5.png)


**KneeAngle.py** will show frontal knee angle for left or right leg. Knee frontal plane movement should be between 170 and 190 degrees during single leg squat. The drawing  indicates (green/red) if frontal angle is inside or outside of the wanted motion range. 


Range ok                  |  Out of range
:-------------------------:|:-------------------------:
![image](https://user-images.githubusercontent.com/11043247/150091572-619a3d6a-205b-4c5b-b9eb-a09bbd88629b.png)  |  ![image](https://user-images.githubusercontent.com/11043247/150106338-236e9877-a37a-4ace-b66f-ceb22b636b33.png)

**SquatCounter.py** will count reps for squat movements. A progression bar is visible on the right side of the screen. When progresssion goes to 0 and back to 100, one rep will be counted. The progression is based on relative distance between hip and ankle landmarks. 100 % distance is calculated when person is standing with straight leg. 75 % distance is counted as one rep for normal squats (90 degree knee angle) and 50 % is calculated for a rep for pistol squats. 

![image](https://user-images.githubusercontent.com/11043247/150110743-e6ef2d50-30c9-47f0-a4ad-1bb6dedfdd8d.png)
