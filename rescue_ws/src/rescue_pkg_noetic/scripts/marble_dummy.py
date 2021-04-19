#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import location_command
from rescue_pkg_noetic.msg import co2

def co2_callback(co2_msg):
    min_co2 = 1500 # ppm

    if co2_msg.ppm > min_co2:
        rospy.loginfo('CO2 message received: %4.2f ppm, CO2 found',co2_msg.ppm)
    else:
        rospy.loginfo('CO2 message received: %4.2f ppm, CO2 not found',co2_msg.ppm)

# def return_callback(return_msg):
#     rospy.loginfo('Return message received: %s',return_msg.data)

def init():
    rospy.init_node('marble_dummy')#, anonymous=True)

    # rospy.Subscriber('return', String, return_callback)

    rospy.Subscriber('co2_data',co2, co2_callback)

def spin():
    pub = rospy.Publisher('location_command', location_command, queue_size=10)
    
    # more publishers here
    rate = rospy.Rate(2) # hz

    location_msg = location_command()
    location_msg.header.stamp = rospy.Time.now()
    location_msg.type_flag = "a"
    location_msg.coord1 = 210
    location_msg.coord2 = 360
    location_msg.coord3 = 1.5

    rospy.sleep(2)
    rospy.loginfo('Coordinates sent: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)
    
    pub.publish(location_msg)
    rospy.spin()


    # while not rospy.is_shutdown():
    #     # hello_str = "location is x y z %s" % rospy.get_time()

    #     location_msg = location_command()
    #     location_msg.header.stamp = rospy.Time.now()
    #     location_msg.type_flag = "a"
    #     location_msg.coord1 = 210
    #     location_msg.coord2 = 360
    #     location_msg.coord3 = 1.5

    #     rospy.loginfo('Coordinates sent: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)
        
    #     pub.publish(location_msg)
    #     rate.sleep()

# def listener():

#     rospy.spin()

if __name__ == '__main__':
    try:
        init()
        spin()
    except rospy.ROSInterruptException:
        pass
