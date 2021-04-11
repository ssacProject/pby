#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
#import jetbot_camera
state = 0
def go_bot(state):
    state = 1
    while True:
        print("go_bot")
        
def callback_1(msg):
    if msg.data == 1:
        msg.data

        if state == 1:
        go_bot(state)
        print("ok")
        return 1
    else:
        print("no")
    #print(msg.data)

rospy.init_node('topic_subscriber')

sub = rospy.Subscriber('counter', Int32, callback_1)
print("sub", sub)
#while sub != 1:
#    print("wait")    
#if sub == 1:
#    print("ok")
#else:
#    print("no")

rospy.spin()

