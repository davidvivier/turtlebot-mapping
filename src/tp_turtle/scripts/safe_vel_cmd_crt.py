#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import Bool

pub = rospy.Publisher('cmd_vel_safe_output', Twist, queue_size=0)

debugPub = rospy.Publisher('/debug', String, queue_size=0)

min_dist = 0.5

em_stop = False

def v_max(d):
    return -0.5 + 1*d

def cmd_vel_callback(data):
    global em_stop
    global min_dist 
    
    debugPub.publish('em_stop = {}'.format(em_stop))
    if em_stop == True:
        pub.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
        debugPub.publish('stopping...\n')
    elif (data.linear.x > 0. and min_dist >= 11.):
        data.linear.x = 0.1
        debugPub.publish('reduced speed\n')
    else:
        data.linear.x = min( v_max(min_dist), data.linear.x)
        debugPub.publish('normal mode')
    
    pub.publish(data)

def min_dist_callback(data):
    global min_dist
    min_dist = float(data.data)

def em_stop_callback(data):
    global em_stop
    em_stop = data

def listener():

    rospy.init_node('safe_vel_cmd_crt', anonymous=True)

    rospy.Subscriber('/cmd_vel_safe_input', Twist, cmd_vel_callback)

    rospy.Subscriber('/min_dist', String, min_dist_callback)

    rospy.Subscriber('/em_stop', Bool, em_stop_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
