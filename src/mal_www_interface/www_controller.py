#! coding:utf-8

import sys
import time
import random

from socketIO_client import SocketIO, LoggingNamespace
import rospy

from std_msgs.msg import String
from mal_msgs.msg import (
    ArmServoMovement,
    LegServoMovement,
    Movement
    )

class WWWController(object):

    LEG_SERVO_TOPIC = "/mal_control/control_leg_servo"
    MOVEMENT_TOPIC = "/mal_control/command"
    FIXED_DURATION = 1.0

    def __init__(self, node_name="www_controller", fps=30):
        rospy.init_node(node_name)
        self.r = rospy.Rate(fps)

        self.move_pub = rospy.Publisher(self.MOVEMENT_TOPIC, Movement, queue_size=10)

        self.setup_socketio()
        
    def main(self):

        mov = [Movement.FRONT, Movement.FRONT_LEFT, Movement.FRONT_RIGHT, Movement.BACK, Movement.BACK_LEFT, Movement.BACK_RIGHT, Movement.ROLL_RIGHT, Movement.ROLL_LEFT, Movement.STOP]

        rospy.loginfo("Starting socket IO Message -------")
        self.socketIO.wait()


    def setup_socketio(self):
        self.socketIO = SocketIO('localhost', 80, LoggingNamespace)
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('reconnect', self.on_reconnect)
        self.socketIO.on('/mal_net_control/direction', self.on_control_response)

    def on_connect(self):
        print('connect')
    
    def on_disconnect(self):
        print('disconnect')
        
    def on_reconnect(self):
        print('reconnect')
        exit()
    
    def on_control_response(self, *args):

        mov = args[0]['data']

        if "STOP" == mov:
            self.publish_movement(Movement.STOP, self.FIXED_DURATION)
            time.sleep(self.FIXED_DURATION)

        if "BACK" == mov:
            self.publish_movement(Movement.BACK, self.FIXED_DURATION)
            time.sleep(self.FIXED_DURATION)

        if "FRONT" == mov:
            self.publish_movement(Movement.FRONT, self.FIXED_DURATION)
            time.sleep(self.FIXED_DURATION)

        if "ROLL_RIGHT" == mov:
            self.publish_movement(Movement.ROLL_RIGHT, self.FIXED_DURATION)
            time.sleep(self.FIXED_DURATION)

        if "ROLL_LEFT" == mov:
            self.publish_movement(Movement.ROLL_LEFT, self.FIXED_DURATION)
            time.sleep(self.FIXED_DURATION)

    def publish_movement(self, direction, duration):
        rospy.loginfo("Direction : " + str(direction) + ", Duration : " + str(duration))

        movement = Movement()
        movement.movement = direction
        movement.duration =  duration
        self.move_pub.publish(movement)
