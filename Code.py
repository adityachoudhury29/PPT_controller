from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import pyautogui
import subprocess

# Ensure the correct path to the presentation
presentation_path = "./zani.pptx"

# Use `xdg-open` to open the PowerPoint presentation in LibreOffice Impress
subprocess.Popen(["xdg-open", presentation_path])

# Allow some time for the presentation to open
cv2.waitKey(2000)

# Parameters
width, height = 900, 720
gestureThreshold = 300

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 20
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False

while True:
    # Get image frame
    success, img = cap.read()

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw

    if hands and buttonPressed is False:  # If hand is detected
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 1, 1, 1, 1]:
                print("Next")
                buttonPressed = True
                pyautogui.press('right')  # Simulate pressing the right arrow key

            if fingers == [1, 0, 0, 0, 0]:
                print("Previous")
                buttonPressed = True
                pyautogui.press('left')  # Simulate pressing the left arrow key

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(img, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
