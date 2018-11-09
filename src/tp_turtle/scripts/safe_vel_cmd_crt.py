#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

pub = rospy.Publisher('cmd_vel_safe_output', Twist, queue_size=0)

def callback(data):
    pub.publish(data)

def listener():

    rospy.init_node('safe_vel_cmd_crt', anonymous=True)

    rospy.Subscriber('/cmd_vel_safe_input', Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
