#! /usr/bin/python

import math

import numpy as np
import rospy
from geometry_msgs.msg import Twist
from rospy import Publisher, Subscriber
from turtlesim.msg import Pose

c1 = 1  # rospy.get_param('~vel_coef')
c2 = 1  # <rospy.get_param('~ang_coef')
c3 = 2  # rospy.get_param('~max_vel')


class Follower:
    def __init__(self):
        self.pub2 = Publisher('/leo/cmd_vel', Twist, queue_size=10)
        self.sub2 = Subscriber('/leo/pose', Pose, self.update)
        self.sub1 = Subscriber('/turtle1/pose', Pose, self.handle)
        self.pose = Pose()

    def update(self, my_pose):
        self.pose = my_pose

    def handle(self, pose):
        msg = Twist()
        dist = np.sqrt((pose.y - self.pose.y) ** 2 + (pose.x - self.pose.x) ** 2)
        eps = 1e-4

        new_theta = math.atan2(pose.y - self.pose.y, pose.x - self.pose.x)
        ang = (new_theta - self.pose.theta)

        while ang > np.pi:
            ang -= 2 * np.pi
        while ang < - np.pi:
            ang += 2 * np.pi

        msg.linear.x = min(c1 * dist, c3)
        msg.angular.z = c2 * ang

        if dist > eps:
            self.pub2.publish(msg)


rospy.init_node('follower')
Follower()

rospy.spin()
