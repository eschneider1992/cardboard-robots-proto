#!/usr/bin/env python

import cv2
import serial
import sys, select, termios, tty
import threading

from numpy import pi
from sys import argv
from copy import deepcopy
from time import sleep
from random import random


class armThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.settings = termios.tcgetattr(sys.stdin)
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600)
        except:
            pass # self.ser = serial.Serial('/dev/ttyACM1', 9600)

    def run(self):
        while 1:
            key = self.getKey()
            if key == '\x03':
                break

            if key == 'w' or key == 's' or key == 'd' or key == 'a':
                print "Would have printed " + key
                # self.ser.write(key)

            print "Got a key!"

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key


class sensorThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cap = cv2.VideoCapture(1)

    def run(self):
        while 1:
            s1 = random() * 255
            s2 = random() * 255
            flag = self.display_video(s1, s2)

            sleep(0.1)

            if flag:
                break

    # Assumes the sensors are 0-255 integers off the Arduino
    def display_video(self, left_sense, right_sense):
        ret, frame = self.cap.read()
        height, width = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        color = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        display_img = frame

        edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
        minLineLength = 500
        maxLineGap = 25
        lines = cv2.HoughLinesP(edges, 5, pi/120, 100, minLineLength, maxLineGap)
        try:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(display_img, (x1, y1), (x2, y2), (0, 255, 0), 4)
        except TypeError:
            pass

        # cv2.rectangle(img, pt1, pt2, color, thickness)
        rec_color = (255, 0, 200)
        rec_thick = 35
        scale = 1.8
        cv2.rectangle(display_img, (rec_thick / 2, height),
                      (rec_thick / 2, height - int(left_sense * scale)),
                      rec_color, rec_thick)
        cv2.rectangle(display_img, (width - rec_thick / 2, height),
                      (width - rec_thick / 2, height - int(right_sense * scale)),
                      rec_color, rec_thick)

        # Display the resulting frame
        # cv2.imshow('frame', frame)
        cv2.imshow('display_image', display_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        else:
            return False


if __name__ == '__main__':
    arm = armThread(1, "Arm thread")
    sensor = sensorThread(2, "Sensor thread")
    
    sensor.start()
    arm.start()