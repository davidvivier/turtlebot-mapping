#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

pub = rospy.Publisher('cmd_vel_safe_output', Twist, queue_size=0)

min_dist = 0.5

def v_max(d):
    return -0.5 + 1*d

def cmd_vel_callback(data):
    global min_dist 
    rospy.loginfo(rospy.get_caller_id() + 'min_dist : %f ', min_dist)
    rospy.loginfo(rospy.get_caller_id() + 'x before : %f ', data.linear.x)
    data.linear.x = min( v_max(min_dist), data.linear.x)
    rospy.loginfo(rospy.get_caller_id() + 'x after : %f ', data.linear.x)

    pub.publish(data)

def min_dist_callback(data):
    global min_dist
    min_dist = float(data.data)

def listener():

    rospy.init_node('safe_vel_cmd_crt', anonymous=True)

    rospy.Subscriber('/cmd_vel_safe_input', Twist, cmd_vel_callback)

    rospy.Subscriber('/min_dist', String, min_dist_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
