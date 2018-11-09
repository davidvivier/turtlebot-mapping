#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

pub = rospy.Publisher('min_dist', String, queue_size=0)

def callback(data):
    values = [ v for v in data.ranges if str(v) != 'nan' ]
    if (len(values) > 0):
        min_dist = min(values)
        rospy.loginfo(rospy.get_caller_id() + 'Minimal distance %f ', min_dist)
        pub.publish(str(min_dist))

def listener():

    rospy.init_node('min_dist', anonymous=True)

    rospy.Subscriber('/scan', LaserScan, callback)



    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
