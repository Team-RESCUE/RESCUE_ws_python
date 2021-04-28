#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import location_command
from rescue_pkg_noetic.msg import co2
from rescue_pkg_noetic.msg import video

def co2_callback(co2_msg):
    min_co2 = 2000 # ppm

    if co2_msg.ppm > min_co2:
        rospy.loginfo('MARBLE: CO2 message received: %4.2f ppm, CO2 found above threshold',co2_msg.ppm)
    else:
        rospy.loginfo('MARBLE: CO2 message received: %4.2f ppm, CO2 not found above threshold',co2_msg.ppm)


def video_callback(video_msg):
    rospy.loginfo('MARBLE: Placeholder video message received: %s',video_msg.msg)

def rescue_status_callback(status_msg):
    rospy.loginfo('MARBLE: Status message received: %s',status_msg)


def init():
    rospy.init_node('marble_dummy')#, anonymous=True)

    # rospy.Subscriber('return', String, return_callback)

    rospy.Subscriber('co2_data', co2, co2_callback)

    rospy.Subscriber('video_data', video, video_callback)

    rospy.Subscriber('rescue_status', String, rescue_status_callback)


def spin():
    pub = rospy.Publisher('location_command', location_command, queue_size=10)
    
    # more publishers here
    rate = rospy.Rate(2) # hz

    location_msg = location_command()
    location_msg.header.stamp = rospy.Time.now()
    location_msg.type_flag = rospy.get_param('type')
    location_msg.coord1 = rospy.get_param('coord1')
    location_msg.coord2 = rospy.get_param('coord2')
    location_msg.coord3 = rospy.get_param('coord3')

    rospy.sleep(1)
    rospy.loginfo('MARBLE: Coordinates sent: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)
    
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
