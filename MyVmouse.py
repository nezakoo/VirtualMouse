import cv2
import mediapipe
import numpy
import time
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
import math

# Video capture. 0 - for the internal webcam, 1 - for the external
cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands  # Initializing mediapipe
# Object of mediapipe with "arguments for the hands module"
mainHand = initHand.Hands(
    max_num_hands=1,
    min_detection_confidence=0.1,
    min_tracking_confidence=0.95)
# Object to draw the connections between each finger index
draw = mediapipe.solutions.drawing_utils
# Outputs the high and width of the screen
wScr, hScr = get_monitors()[0].width, get_monitors()[0].height
pX, pY = 0, 0  # Previous x and y location
pTime = 0  # Time for the FPS section
cTime = 0  # Time for the FPS section
mouse = Controller()  # mouse controller pynput
smoothening = 1.7  # random value for the smoothing


def handLandmarks(colorImg):
    landmarkList = []  # Default values if no landmarks are tracked

    # Object for processing the video input
    landmarkPositions = mainHand.process(colorImg)
    # Stores the out of the processing object (returns False on empty)
    landmarkCheck = landmarkPositions.multi_hand_landmarks
    if landmarkCheck:  # Checks if landmarks are tracked
        for hand in landmarkCheck:  # Landmarks for each hand
            # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)
            for index, landmark in enumerate(hand.landmark):
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS,
                                    draw.DrawingSpec(
                                        color=(121, 22, 76), thickness=2, circle_radius=4),
                                    draw.DrawingSpec(
                                        color=(250, 44, 250), thickness=2, circle_radius=2))  # Draws each individual index on the hand with connections
                h, w, c = img.shape  # Height, width and channel on the image
                # print(img.shape)
                # Converts the decimal coordinates relative to the image for each index
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)
                # Adding index and its coordinates to a list
                landmarkList.append([index, centerX, centerY])

    return landmarkList


def fingers(landmarks):
    fingerTips = []  # To store 4 sets of 1s or 0s
    tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger

    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    # Check if fingers are up except the thumb
    for id in range(1, 5):
        # Checks to see if the tip of the finger is higher than the joint
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips


while True:
    capStatus, img = cap.read()  # Reads frames from the camera
    # Changes the format of the frames from BGR to RGB
    # # if you want to resize the image:
    # dim = (wScr, hScr) # width, height
    # resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)
    # FPS section start
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    # FPS section end
    if len(lmList) != 0:
        # Gets index 8s x and y values (skips index value because it starts from 1)
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Calling the fingers function to check which fingers are up
        finger = fingers(lmList)

        # the length between [P]oint and [M]iddle fingers
        lengthPM = math.hypot(x2 - x1, y2 - y1)

        # Converts the width of the window relative to the screen width
        x3 = int(numpy.interp(
            x1, (wScr/10, wScr/smoothening - wScr/10), (0, wScr)))
        # Converts the height of the window relative to the screen height
        y3 = int(numpy.interp(
            y1, (hScr/10, hScr/smoothening - hScr/10), (0, hScr)))

        # Checks to see if the pointing finger is up and thumb finger is down
        if finger[1] == 1 and finger[2] == 0 and finger[3] == 0 and finger[0] == 0 and finger[4] == 0:
            # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)
            mouse.position = (wScr-x3, y3)

        # Left click
        if finger[1] == 1 and finger[2] == 1 and finger[0] == 0:
            mouse.click(Button.left, 1)
            time.sleep(0.7)  # Sleep to prevent the click flow

        # Double left click
        if finger[1] == 1 and finger[2] == 1 and lengthPM < 40 and finger[0] == 0:
            mouse.click(Button.left, 2)
            time.sleep(0.7)  # Sleep to prevent the click flow

        # Right click
        if finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[0] == 0 and finger[4] == 0:
            mouse.click(Button.right, 1)
            time.sleep(0.7)  # Sleep to prevent the click flow

        if finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
            # scroll on all directions
            dx, dy = (pX - x3), (pY - y3)
            mouse.scroll(-dx/1.5, -dy/1.5)
            pX, pY = x3, y3  # Keep previous coordinates

        if finger[1] == 0 and finger[2] == 1 and finger[3] == 0 and finger[0] == 0 and finger[4] == 0:
            print('Exiting on the gestue')
            exit()  # temp for easy exit

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# TBD add the multiple monitor feature by dividing the capture screen to areas

# if both point and middle fingers up -- scroll. by moving them up or down --done
