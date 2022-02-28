#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tello_interfaces.action import Move
from tello_interfaces.srv import HexaCmd
from tello_msgs.msg import FlightCondition
from tello_msgs.srv import TelloAction
from rclpy.action import ActionServer
from functools import partial
import queue
import numpy as np


class MoveServerNode(Node): 
    def __init__(self):
        super().__init__("move_server") 

        self.origin = np.array([0,0,0]) # x,y,z
        self.last_time_ = queue.Queue(2)  #The max size is 2. FIFO
        self.dt_ = 0 # initial value.
        self.count = 0

        self.flight_condition_ = None
        self.flight_condition_subscriber_ = self.create_subscription(
            FlightCondition, "drone1/flight_condition", self.callback_flight_condition, 10)

        self.dir = None
        self.dist = 0
        self.travel_distance = np.array([0.,0.,0.,0.])  # x,y,z - coordinate in meter, z-axis in radian

        self.server_ = self.create_service(HexaCmd, "drone1/move_cmd", self.callback_HexaCmd)
        self.ready = False

        self.control_loop_timer_ = self.create_timer(
            0.1, self.control_loop)  # we call control_loop fn every 10hz

        # self._action_server = ActionServer(
        #     self,
        #     Move,
        #     'move',
        #     self.callback_move)

    def callback_HexaCmd(self, request, response):
        
        self.dir = request.dir
        self.dist = request.dist
        self.get_logger().info("Moving toward "+self.dir + "direction, "+ str(self.dist)+"m")

        response.result = True

        self.ready = True
        self.remain = np.inf
        return response


    # def call_move_cmd_server(self, dir, dist):
    #     client = self.create_client(HexaCmd, "drone1/move_cmd")
    #     while not client.wait_for_service(1.0):
    #         self.get_logger().warn("Waiting for Server drone1/move_cmd...")
    #     request = HexaCmd.Request()
    #     request.dir = dir
    #     request.dist = dist


    def callback_flight_condition(self, msg):
        try:

            self.flight_condition_ = msg
            current_time = msg.header.stamp.sec + msg.header.stamp.nanosec * 10**-9
            
            if self.last_time_.empty():
                return self.last_time_.put(msg.header.stamp.sec + msg.header.stamp.nanosec * 10**-9)
            self.dt_ = current_time - self.last_time_.get() 
            if self.dt_ <= 0: # if dt is negative or zero, stop the function. (only update current time)
                return self.last_time_.put(msg.header.stamp.sec + msg.header.stamp.nanosec * 10**-9)

            self.travel_distance += msg.vgx*self.dt_ + 0.5*msg.agx*self.dt_**2, msg.vgy*self.dt_ + 0.5*msg.agy*self.dt_**2, msg.vgz*self.dt_ + 0.5*(msg.agz-9.8)*self.dt_**2, msg.wgz*self.dt_ + 0.5*msg.awgz*self.dt_**2  # 0.5 * 1000mm

            self.last_time_.put(msg.header.stamp.sec + msg.header.stamp.nanosec * 10**-9)
            if self.last_time_.full(): # keep only one element 
                self.last_time.get()

            # self.get_logger().info('travle distance: '+str(self.travel_distance))
            
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))

    
    def control_loop(self):
        if self.ready:
            self.get_logger().info('Move to target position...')
            self.get_logger().info('remain: '+ str(self.remain))
        else: 
            return 1
        
        if abs(self.remain) > 0.1:
            self.call_pid_control(self)

        elif abs(self.remain) < 0.1 and self.count <= 30:
            self.get_logger().info('Moving around the target')
            self.count += 1
            self.call_pid_control(self)
            
        elif self.ready: 
            
            self.get_logger().info('Successfully moved to the target location!')
            client = self.create_client(TelloAction, "/drone1/tello_action")
            while not client.wait_for_service(1.0):
                self.get_logger().warn("Waiting for Server of tello_action_cmd")
            request = TelloAction.Request()
            request.cmd = "rc 0 0 0 0"
            future = client.call_async(request)
            future.done()
            # rclpy.shutdown()
            self.ready = False
        else:
            self.get_logger().warn("Waiting for the next cmd")

    def call_pid_control(self, future):

        if self.dir=="xy":
            self.remain = self.dist - self.travel_distance[-1]
        elif self.dir=="x":
            self.remain = self.dist - self.travel_distance[0]
        elif self.dir=="y":
            self.remain = self.dist - self.travel_distance[1]
        elif self.dir=="z":
            self.remain = self.dist - self.travel_distance[2]
        else:
            self.get_logger().warn('Wrong direction! Direction should be x or y or z or xy (z-axis)')
        
        client = self.create_client(TelloAction, "/drone1/tello_action")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server of tello_action_cmd")
        
        Kd = 0.1
        Kp = 0.1
        Ki = 0.01

        if not self.dt_: self.dt_ = 0.01
        value = self.remain*(Kp)#+Ki/self.dt_+Kd*self.dt_)

        request = TelloAction.Request()
        if self.dir=="x": 
            request.cmd = "rc %0.03f 0 0 0"%(value)
            self.get_logger().info(f"{request.cmd} in {self.dir}")
        elif self.dir=="y": 
            request.cmd = "rc 0 %0.03f 0 0"%(value)
            self.get_logger().info(f"{request.cmd} in {self.dir}")
        if self.dir=="z": 
            request.cmd = "rc 0 0 %0.03f 0"%(value)
            self.get_logger().info(f"{request.cmd} in {self.dir}")
        if self.dir=="xy": 
            request.cmd = "rc 0 0 0 %0.03f"%(value)
            self.get_logger().info(f"{request.cmd} in {self.dir}")

        future = client.call_async(request)
        future.add_done_callback(
            partial(self.callback_pid_control, self.dir, self.remain)) # dir, offset should be deleted.

    def callback_pid_control(self, a, b, future):
        try:
            self.get_logger().info(str(a) + " direction and " +
                                   str(float(b)) + "m")
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))

def main(args=None):
    rclpy.init(args=args)
    node = MoveServerNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
