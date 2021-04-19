#!/usr/bin/env python

import rospy
# from std_msgs.msg import String
from rescue_pkg_noetic.msg import location_command

def callback(location_msg):
    rospy.loginfo('Coordinates received: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('RESCUE_main', anonymous=True)

    rospy.Subscriber('location_command', location_command, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
