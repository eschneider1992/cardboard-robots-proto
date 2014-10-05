#!/usr/bin/env python

import cv2
import serial
import sys, select, termios, tty
import threading
import time

from numpy import pi
from sys import argv
from copy import deepcopy
from time import sleep
from random import random
from arduino import Arduino



class armThread(threading.Thread):
    def __init__(self, threadID, name, arduino):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.arduino = arduino
        self.settings = termios.tcgetattr(sys.stdin)

    def run(self):
        servo_pwm = 0
        motor_pwm = 1

        while 1:
            key = self.getKey()
            if key == '\x03':
                self.arduino.setServo(motor_pwm, 90)
                break

            if key == 'a':
                self.arduino.setServo(servo_pwm, 127) # limit because converted to char on arduino
            elif key == 'd':
                self.arduino.setServo(servo_pwm, 0)
            elif key == 'w':
                self.arduino.setServo(motor_pwm, 127)
            elif key == 'x':
                self.arduino.setServo(motor_pwm, 53)
            else:
                self.arduino.setServo(motor_pwm, 90)

            print "Got a key!: " + key

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key


class sensorThread (threading.Thread):
    def __init__(self, threadID, name, arduino):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.arduino = arduino
        try:
            self.cap = cv2.VideoCapture(1)
        except:
            pass

    def run(self):
        flag = False
        while 1:
            try:
                s1 = float(self.arduino.analogRead(0))
                s2 = float(self.arduino.analogRead(1))
            except:
                s1 = 0
                s2 = 0
            try:
                flag = self.display_video(s1, s2)
            except AttributeError:
                flag = True

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
        scale = 0.62 # sensitivity of distance sensors

        p1 = (rec_thick / 2, height)
        p2 = (rec_thick / 2, height - int(left_sense * scale))
        cv2.rectangle(display_img, p1, p2, rec_color, rec_thick)
        
        p1 = (width - rec_thick / 2, height)
        p2 = (width - rec_thick / 2, height - int(right_sense * scale))
        cv2.rectangle(display_img, (width - rec_thick / 2, height),
                      (width - rec_thick / 2, height - int(right_sense * scale)),
                      rec_color, rec_thick)

        # Display the resulting frame
        # cv2.imshow('frame', frame)
        cv2.imshow('display_image', display_img)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     return True
        # else:
        #     return False


if __name__ == '__main__':
    try:
        arduino = Arduino('/dev/ttyACM0')
    except:
        arduino = Arduino('/dev/ttyACM1')
    arduino.output([2]) # This is a default to keep from hanging in setup


    print "Starting the arm thread"
    arm = armThread(1, "Arm thread", arduino)
    print "Starting the sensor thread"
    sensor = sensorThread(2, "Sensor thread", arduino)
    
    sensor.start()
    arm.start()