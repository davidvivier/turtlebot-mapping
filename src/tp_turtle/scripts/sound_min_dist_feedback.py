#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from kobuki_msgs.msg import Led 
from kobuki_msgs.msg import Sound 

soundPub = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size=0)
ledPub = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=0)

led_state = 0



def callback(data):

    min_dist = float(data.data)

    period = 0.06 + min_dist*0.25/1.1
    global rate
    rate = rospy.Rate(2/(period))

    rospy.loginfo(rospy.get_caller_id() + 'Dist = %f Period = %f Rate = %f', min_dist, period, 2/(period))



def toggle_led():
    global led_state
    led_state = 0 if led_state == 1 else 1
    ledPub.publish(led_state)

def listener():
    global led_state

    rospy.init_node('sound_min_dist_feedback', anonymous=True)

    rospy.Subscriber('/min_dist', String, callback)

    global rate
    rate = rospy.Rate(1)
    
    while not rospy.is_shutdown():
        toggle_led()
        soundPub.publish(3)
        rate.sleep()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
