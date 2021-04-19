#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import location_command
from rescue_pkg_noetic.msg import co2

def loc_callback(location_msg):
    rospy.loginfo('Coordinates received: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)
    # return_msg = 'RETURN'
    # rospy.loginfo('Return message sent: %s',return_msg)
    # return_pub = rospy.Publisher('return', String, queue_size=10)
    # return_pub.publish(return_msg)
    # rospy.Rate(2).sleep()

def init():
    rospy.init_node('RESCUE_main')#, anonymous=True)

    rospy.Subscriber('location_command', location_command, loc_callback)

# def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    # rospy.init_node('RESCUE_main', anonymous=True)

    # rospy.Subscriber('location_command', location_command, callback)

    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()

def spin():
    co2_pub = rospy.Publisher('co2_data', co2, queue_size=10)

    co2_msg = co2()
    co2_msg.ppm = 1400
    rospy.loginfo("CO2 data sent: %4.2f ppm",co2_msg.ppm)

    rospy.sleep(2)
    co2_pub.publish(co2_msg)
    rospy.spin()
    # rate = rospy.Rate(2) # hz

    # while not rospy.is_shutdown():
    #     co2_msg = co2()
    #     co2_msg.ppm = 1400
    #     rospy.loginfo("CO2 data sent: %4.2f ppm",co2_msg.ppm)

    #     co2_pub.publish(co2_msg)
    #     rate.sleep()


if __name__ == '__main__':
    try:
        init()
        spin()
    except rospy.ROSInterruptException:
        pass