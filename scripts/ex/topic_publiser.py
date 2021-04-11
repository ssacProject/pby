#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32

rospy.init_node('topic_publisher')

pub = rospy.Publisher('counter', Int32)

rate = rospy.Rate(2) #2Hz

count = 1
for _ in range(5):
    pub.publish(count)
    count += 1
    rate.sleep()
