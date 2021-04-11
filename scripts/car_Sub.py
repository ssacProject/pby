#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
import jetbot_camera as jc

def callback(msg):
    if msg.data == 3:
        print("go")
        jc.Video()
        
    print(msg.data)
 

rospy.init_node('topic_subscriber')

sub = rospy.Subscriber('counter', Int32, callback)

rospy.spin()

