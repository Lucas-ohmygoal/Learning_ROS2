#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from learning_interface.srv import AddTwoInts

class AdderClient(Node):
    def __init__(self, name):
        super().__init__(name)
        self.client = self.create_client(AddTwoInts, "add_two_ints")
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting...")
        self.request = AddTwoInts.Request()

    def send_request(self):
        self.request.a = int(sys.argv[1])
        self.request.b = int(sys.argv[2])
        self.future = self.client.call_async(self.request)

def main(args=None):
    rclpy.init(args=args)
    node = AdderClient("service_adder_client")
    node.send_request()

    while rclpy.ok():

        if node.future.done():
            try:
                response = node.future.result()
            except Exception as e:
                node.get_logger().info('service call failed %r' % (e,))
            else:
                node.get_logger().info('Result for add_two_ints: %d + %d = %d' % (
                    node.request.a, node.request.b, response.sum
                ))
            break
    
    node.destroy_node()
    rclpy.shutdown()

