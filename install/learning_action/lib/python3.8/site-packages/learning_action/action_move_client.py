#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from learning_interface.action import MoveCircle


class MoveCircleActionClient(Node):
    def __init__(self, name):
        super().__init__(name)
        self._action_client = ActionClient(self, MoveCircle, "move_circle")

    def send_goal(self, enable):
        goal_msg = MoveCircle.Goal()
        goal_msg.enable = enable

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, futrue):
        goal_handle = futrue.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected :(")
            return
        self.get_logger().info("Goal accepted :)")

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info("Result: {%d}" % result.finish)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info("Received feedback {%d}" % feedback.state)

def main(args=None):
    rclpy.init(args=args)
    node = MoveCircleActionClient("action_move_client")
    node.send_goal(True)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()