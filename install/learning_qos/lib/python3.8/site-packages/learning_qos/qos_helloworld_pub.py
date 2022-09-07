#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class PublisherNode(Node):
    def __init__(self, name):
        super().__init__(name)
        
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.pub = self.create_publisher(String, "chatter", qos_profile)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = "Hello World!"
        self.pub.publish(msg)
        self.get_logger().info('publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode("qos_helloworld_pub")
    rclpy.spin(node)
    node.destroy_publisher()
    rclpy.shutdown()