'''
Mask Detector Robot

A Python code for detecting the face masks depending on HSV color system using OpenCV.

The robot will capture an image using the attached camera with TXT controller from fischertechnik.

Done By: Eng. Meqdad Darwish
'''
import cv2 as cv
import ftrobopy
import time
import numpy as np


txt = ftrobopy.ftrobopy('192.168.7.2', 65000)  # USB

ultrasonic_sensor = txt.ultrasonic(6)  # I6
stop_condition = False

M1 = txt.motor(1)  # Create a motor object (M1)
M2 = txt.motor(2)  # Create a motor object (M2)
M1.setSpeed(-280)  # Set speed
M2.setSpeed(268)  # Set speed
txt.updateWait()

while not stop_condition:
    txt.updateWait()
    distance = ultrasonic_sensor.distance()
    s = "Measured distance: {:5f}".format(distance)
    print(s, end='\r')
    if distance <= 22:
        stop_condition = True
        M1.stop()
        M2.stop()
        print("Stopped")

if stop_condition is True:
    txt.startCameraOnline()
    time.sleep(3)
    im = "TXTimage.jpg"
    pic = txt.getCameraFrame()
    time.sleep(2)

    with open(im, 'wb') as f:
        f.write(bytearray(pic))

    time.sleep(1)
    txt.stopCameraOnline()

    im = cv.imread(im)

    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)

    lower_range = np.array([0, 0, 0])
    upper_range = np.array([40, 40, 40])
    mask = cv.inRange(hsv, lower_range, upper_range)

    cv.imshow('image', im)

    cv.imshow("Mask", mask)

    cv.waitKey(0)
