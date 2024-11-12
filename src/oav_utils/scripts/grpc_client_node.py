#!/usr/bin/env python3

from __future__ import print_function

import os
import random
import logging
import time
import pprint

import grpc
import pygame
import threading

import rpi_motor_pb2
import rpi_motor_pb2_grpc

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class GrpcClient(Node):

    def __init__(self):
        super().__init__('grpc_client_node')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.u = 0.0 # linear 'x' vel. in omni-directional base
        self.v = 0.0 # linear 'y' vel. in omni-directional base
        self.w = 0.0 # linear height vel. in elevator

        self.q = 0.0 # angular pitch setpoint of camera
        self.r = 0.0 # angular yaw vel. in omni-directional base

        self.port = 50201
        self.channel = grpc.insecure_channel('192.168.1.11:'+str(self.port))
        self.client = rpi_motor_pb2_grpc.RPIMotorStub(self.channel)

        self.req = rpi_motor_pb2.StateRequest()
        

    def listener_callback(self, msg):
        self.u = msg.linear.x
        self.v = msg.linear.y
        self.w = msg.linear.z
        
        self.q = msg.angular.y
        self.r = msg.angular.z


        self.req.vel_x = self.u
        self.req.vel_y = self.v
        self.req.vel_yaw = self.r

        self.req.vel_heave = self.w
        self.req.pitch = self.q
        self.req.leds = 0.

        res = self.client.SetState(self.req)
        self.get_logger().info("New velocity input: %f, %f, %f" % (self.u, self.v, self.r))
  
def main(args=None):
    rclpy.init(args=args)
    grpc_client = GrpcClient()
    rclpy.spin(grpc_client)
    grpc_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()