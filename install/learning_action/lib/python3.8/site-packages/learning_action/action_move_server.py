#!/usr/bin/env python3

import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from learning_interface.action import MoveCircle


class MoveCircleActionServer(Node):
    def __init__(self, name):
        super().__init__(name)
        self._action_server = ActionServer(
            self,
            MoveCircle,
            "move_circle",
            self.execute_callbacks
        )

    def execute_callbacks(self, goal_handle):
        self.get_logger().info("Moveing circle...")
        feedback_msg = MoveCircle.Feedback()
        
        for i in range(0, 360, 30):
            feedback_msg.state = i
            self.get_logger().info("Publishing feedback: %d" % feedback_msg.state)
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(0.5)
        
        goal_handle.succeed()
        result = MoveCircle.Result()
        result.finish = True
        return result

def main(args=None):
    rclpy.init(args=args)
    node = MoveCircleActionServer("action_move_server")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()