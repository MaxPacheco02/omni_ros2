#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, Vector3

class TeleopControl(Node):

    def __init__(self):
        super().__init__('teleop_control_node')
        self.jsub = self.create_subscription(
            Joy, '/joy', self.convert_joy, 10
        )

        self.twist_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.twist_msg = Twist()

        self.max_vel  = [1., 1., 1., 1.] # +- for (x,y,z) linear, (z) ang.
        self.curr_vel = [0., 0., 0., 0.]

        self.current_pitch = 7.5

        self.increment = 0.1

    def convert_joy(self, msg):
        # Axes:
        '''
        AXES
        0: y vel. additive -> [1,-1] to [-1,1]
        1: x vel. additive -> original
        3: yaw vel. additive -> [1,-1] to [-1,1]

        7: pitch (cam) vel. additive -> {1,0,-1} to {-1,0,1}

        BUTTONS
        4: lower elevator (boolean)
        5: raise elevator (boolean)
        '''
        # Axes
        u_i = 1
        v_i = 0
        r_i = 3
        q_i = 7

        # Buttons
        z_down_i = 4
        z_up_i = 5

        u = msg.axes[u_i]*1.
        self.curr_vel[0] = max( -self.max_vel[0] , min( u , self.max_vel[0] ))
        v = -msg.axes[v_i]*1.
        self.curr_vel[1] = max( -self.max_vel[1] , min( v , self.max_vel[1] ))
        r = msg.axes[r_i]*1.
        self.curr_vel[3] = max( -self.max_vel[3] , min( r , self.max_vel[3] ))

        z_ = msg.buttons[z_up_i] - msg.buttons[z_down_i]*1.
        self.curr_vel[2] = z_*self.increment
        
        self.current_pitch += -msg.axes[q_i]*self.increment*1.5
        self.current_pitch = max( 5. , min( self.current_pitch , 10. ))
        q = self.current_pitch*1.

        multiplier_x = 0.05
        multiplier_y = 0.01
        multiplier_r = 0.1
        # multiplier_x = 0.5
        # multiplier_y = 0.5
        # multiplier_r = 1.
        
        if abs(u) < 0.1:
            u = 0.
        if abs(v) < 0.1:
            v = 0.
        if abs(r) < 0.1:
            r = 0.

        self.twist_msg = Twist(linear = Vector3(x = u*multiplier_x, y = v*multiplier_y, z = z_),
                               angular = Vector3(x = 0., y = q, z = r*multiplier_r))

        self.twist_pub.publish(self.twist_msg)

def main(args=None):
    rclpy.init(args=args)
    rmn = TeleopControl()
    rclpy.spin(rmn)
    rmn.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()