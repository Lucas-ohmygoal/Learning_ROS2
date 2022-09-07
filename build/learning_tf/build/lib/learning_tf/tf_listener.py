#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
import tf_transformations
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class TFListener(Node):
    def __init__(self, name):
        super().__init__(name)

        self.declare_parameter('source_frame', 'world')
        self.source_frame = self.get_parameter(
            'source_frame').get_parameter_value().string_value
        
        self.declare_parameter('target_frame', 'house')
        self.target_frame = self.get_parameter(
            'target_frame').get_parameter_value().string_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.on_timer)


    def on_timer(self):
        try:
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.source_frame,
                now)
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {self.target_frame} to {self.source_frame}: {ex}')
            return

        
        pos  = trans.transform.translation                          
        quat = trans.transform.rotation                             
        euler = tf_transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
        self.get_logger().info('Get %s --> %s transform: [%f, %f, %f] [%f, %f, %f]' 
          % (self.source_frame, self.target_frame, pos.x, pos.y, pos.z, euler[0], euler[1], euler[2]))

def main(args=None):
    rclpy.init(args=args)                      
    node = TFListener("tf_listener")            
    rclpy.spin(node)                            
    node.destroy_node()                        
    rclpy.shutdown() 