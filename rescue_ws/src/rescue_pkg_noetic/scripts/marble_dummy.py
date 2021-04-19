#!/usr/bin/env python

import rospy
from std_msgs.msg import Header
from rescue_pkg_noetic.msg import location_command

def talker():
    pub = rospy.Publisher('location_command', location_command, queue_size=10)
    
    # more publishers here

    rospy.init_node('marble_dummy', anonymous=True)
    rate = rospy.Rate(10) # 10hz


    while not rospy.is_shutdown():
        # hello_str = "location is x y z %s" % rospy.get_time()

        location_msg = location_command()
        location_msg.header.stamp = rospy.Time.now()
        location_msg.type_flag = "a"
        location_msg.coord1 = 210
        location_msg.coord2 = 360
        location_msg.coord3 = 1.5

        rospy.loginfo('Coordinates sent: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)
        
        pub.publish(location_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
