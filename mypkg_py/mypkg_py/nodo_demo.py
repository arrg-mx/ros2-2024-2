#! /usr/bin/env python3

# import libraries
from typing import List
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from mypkg_interfaces.msg import MyCustom

# declaracion de clases y funciones

class MyNodo(Node):
    def __init__(self):
        super().__init__('mynodo')
        self.qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.mytopic_pub = self.create_publisher(MyCustom, '/mytopic', self.qos_profile)
        self.timer_period = 0.01 # 1/100 segundos
        self.timer = self.create_timer(self.timer_period, self._on_topic_clbk)


    def _on_topic_clbk(self):
        message = MyCustom()
        message.data = "Curso de ROS2 - Personalizado"
        message.valor_f = 3.1415
        message.valor_i = 255
        self.mytopic_pub.publish(message)


def main(args=None):
    # flujo del ciclo de trabajo del nodo
    rclpy.init(args=args) #inicializando el canal de comunicacion del cliente de DDL para mi nodo
    nodo = MyNodo()     #Creo una instancia de mi nodo
    # Operacion/es que necesite el nodo y sus topicos
    rclpy.spin(nodo) # spin -> Mantiene en ejecusion al nodo
    rclpy.shutdown() # Destruye el canal de comunicacion abierto inicialmente

# Punto de entrada

if __name__ == '__main__':
    main()