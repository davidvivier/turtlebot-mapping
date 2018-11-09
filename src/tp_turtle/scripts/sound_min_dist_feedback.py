#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from kobuki_msgs.msg import Led 

#soundPub = rospy.Publisher('', String, queue_size=0)
ledPub = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=0)

led_state = 0

def callback(data):

    min_dist = float(data)


def toggle_led():
    global led_state
    led_state = 0 if led_state == 1 else 1
    ledPub.publish(led_state)

def listener():
    global led_state
    
    rospy.init_node('sound_min_dist_feedback', anonymous=True)

    rospy.Subscriber('/min_dist', String, callback)

    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        toggle_led()
        rate.sleep()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
