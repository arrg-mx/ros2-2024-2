import rclpy

from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from std_msgs.msg import String

class DofbotNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.qosprofile = QoSProfile(
            reliability = QoSReliabilityPolicy.RELIABLE,
            history = QoSHistoryPolicy.KEEP_LAST, 
            depth=10 # queue
        )
        self.demo_pub = self.create_publisher(String, '/status', self.qosprofile)
        self.timer_period = 0.01  # 1/100 segundos
        self.timer = self.create_timer(self.timer_period, self._on_timer_clbk)
        self.get_logger().info(f"[dofbot_ctrl]: Node {node_name} created.")

    def _on_timer_clbk(self):
        message = String()
        message.data = f"[Mensaje demo]"
        self.demo_pub.publish(message)
        

def main(args=None):
    rclpy.init(args=args)
    node = DofbotNode('dofbot_nodo_demo')
    rclpy.spin(node)
    node.destroy_node()

if __name__ == '__main__':
    main()