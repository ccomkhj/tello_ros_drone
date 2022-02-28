#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tello_interfaces.action import Move
from rclpy.action import ActionClient


class MoveClientNode(Node): 
    def __init__(self):
        super().__init__("move_client") 
        self._action_client = ActionClient(
            self,
            Move,
            'move')
    
    def send_goal(self, direction, distance):
        assert direction in ['x','y','z','xy'], "direction should be x or y or z or xy"
        goal_msg = Move.Goal()
        goal_msg.dir = direction
        goal_msg.dist = distance
        self._action_client.wait_for_server()
        return self._action_client.send_goal_async(goal_msg)


def main(args=None):
    rclpy.init(args=args)
    node = MoveClientNode() 
    future = node.send_goal('x', 100.0)
    rclpy.spin_until_future_complete(node, future)


if __name__ == "__main__":
    main()
