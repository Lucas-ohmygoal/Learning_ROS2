#!/usr/bin/env python3

from platform import node
import rclpy
from rclpy.node import Node

import cv2
import numpy as np


class ObjectDetection(Node):
    def __init__(self, name):
        super().__init__(name)
        self.lower_red = np.array([0, 90, 128])
        self.upper_red = np.array([180, 255, 255])
        self.cap = cv2.VideoCapture(0)

        while rclpy.ok():
            self.ret, self.image = self.cap.read()
            if self.ret == True:
                self.detect_object()

    def detect_object(self):
        hsv_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask_red = cv2.inRange(hsv_img, self.lower_red, self.upper_red)

        contours, hierachy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        
        for cnt in contours:
            if cnt.shape[0] < 150:
                continue

            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.drawContours(self.image, [cnt], -1, (0, 255, 0), 2)
            cv2.circle(self.image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)
        
        cv2.imshow("object", self.image)
        cv2.waitKey(50)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetection("node_object_webcam")
    node.destroy_node()
    rclpy.shutdown()


    