#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import Sound

soundPub = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size=0)

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=0)
    rospy.init_node('collision_warning', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()


def play_sound():
    soundPub.publish(1)


def callback(data):
    bumper = data
    if bumper.state == 1:
        # log 
        rospy.loginfo(rospy.get_caller_id() + 'Front collision detected ')
        # sound
        play_sound()




def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback)



    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
