#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import Sound
from std_msgs.msg import Bool

soundPub = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size=0)
emStopPub = rospy.Publisher('/em_stop', Bool, queue_size=0)

def play_sound():
    soundPub.publish(1)


def callback(data):
    bumper = data
    

    if bumper.state == 1:
        # log 
        rospy.loginfo(rospy.get_caller_id() + 'Front collision detected ')
        # sound
        play_sound()
        emStopPub.publish(True)
    else:
        emStopPub.publish(False)



def listener():

    rospy.init_node('collision_warning', anonymous=True)

    rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback)



    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
