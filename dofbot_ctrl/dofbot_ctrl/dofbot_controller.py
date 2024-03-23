#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import math

class DofbotArmCtrl(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # self._gripper_status = self.create_publisher(JointState, '/joint_states', 10)
        self._gripper_status_pub = self.create_publisher(String, '/gripper_status', 10)
        self._joint_states_sub = self.create_subscription(JointState, '/joint_states', self._on_joint_states_callback, 10)
        self.tol = 0.0174533 # rads = 1 grado
        self.get_logger().debug(f"Node '{node_name}' initialized")

    def _on_joint_states_callback(self, joint_state_msg: JointState):
        gripper_status = String()
        indx_gripper = joint_state_msg.name.index('grip_joint')
        link_value = joint_state_msg.position[indx_gripper]
        
        if abs(link_value) <= self.tol:
            gripper_status.data = "Cerrada"
        elif abs(link_value) <= 1.54 and abs(link_value) >= (1.54 - self.tol):
            gripper_status.data = "Full open"
        else:
            gripper_status.data = "Partial open"
        
        self.get_logger().debug(f"{indx_gripper}[{link_value}]:{gripper_status.data}")

        self._gripper_status_pub.publish(gripper_status)
    
def main(args=None):
    rclpy.init(args=args)
    try:
        arm_ctrl = DofbotArmCtrl('armctrl_node')
        rclpy.spin(arm_ctrl)
        arm_ctrl.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()
