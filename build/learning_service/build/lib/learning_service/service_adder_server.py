#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from learning_interface.srv import AddTwoInts


class AdderServer(Node):
    def __init__(self,name):
        super().__init__(name)
        self.server = self.create_service(AddTwoInts, "add_two_ints", self.adder_callback)

    def adder_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info("Getting request: %d and %d" %(request.a, request.b))
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AdderServer("service_adder_server")
    rclpy.spin(node)
    node.destroy_node
    rclpy.shutdown()