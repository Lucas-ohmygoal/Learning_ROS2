#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class ParameterNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.timer = self.create_timer(2, self.timer_callback)
        self.declare_parameter("robot_name", "mbot")

    def timer_callback(self):
        robot_name_param = self.get_parameter("robot_name").get_parameter_value().string_value
        self.get_logger().info("Hello %s!" % robot_name_param)
        new_name_parameter = rclpy.parameter.Parameter("robot_name",
            rclpy.Parameter.Type.STRING, "mbot"
        )
        all_new_parameters = [new_name_parameter]
        self.set_parameters(all_new_parameters)

def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode("param_declare")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()