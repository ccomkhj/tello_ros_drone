#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

class ImageProcessingNode(Node): 
    def __init__(self):
        super().__init__("image_processing") 

        self.out = cv2.VideoWriter('output.avi', -1, 30.0, (720,960))

        self.flight_condition_subscriber_ = self.create_subscription(
            Image, "drone1/image_raw", self.callback_image_processing, 10)

    def callback_image_processing(self,msg):
        # can access to time using msg.header.stamp

        frame = np.array(msg.data).reshape(msg.height, msg.width, 3) # if msg.encoding is rgb8.
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.out.write(frame)
        cv2.imshow('camera', frame)
        cv2.waitKey(1)




def main(args=None):
    rclpy.init(args=args)
    node = ImageProcessingNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
