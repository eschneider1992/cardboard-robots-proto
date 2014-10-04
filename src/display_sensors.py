#!/usr/bin/env python
import cv2

from numpy import pi
from sys import argv
from copy import deepcopy
from time import sleep


def main(args):
  print ("Press 'q' to quit WHEN FOCUSED ON CV WINDOW")
  
  cap = cv2.VideoCapture(1)

  try:
    while(True):
      # Capture frame-by-frame
      ret, frame = cap.read()

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      color = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
      edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
      minLineLength = 500
      maxLineGap = 25
      lines = cv2.HoughLinesP(edges, 5, pi/120, 100, minLineLength, maxLineGap)
      try:
        for line in lines:
          for x1, y1, x2, y2 in line:
              cv2.line(color, (x1, y1), (x2, y2), (0, 255, 0), 4)
      except TypeError:
        print "Got an empy line variable"

      # Display the resulting frame
      cv2.imshow('frame', frame)
      cv2.imshow('color', color)


      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

      sleep(0.1)


  except KeyboardInterrupt:
    print "Shutting down"

  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
    main(argv)
