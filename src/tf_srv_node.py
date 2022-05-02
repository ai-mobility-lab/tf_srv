#!/usr/bin/env python

## import ros packages
import rospy
import tf
from geometry_msgs.msg import Vector3, Quaternion

## import fundamental packages
import numpy as np
import math

## import service message
from tf_srv.srv import LookupTransform
from tf_srv.srv import TransformPCL

class TransformService():
    def __init__(self):
        # define transform listener
        self.listener = tf.TransformListener()
        ## define service
        self.srv_action = rospy.Service('/tf_srv/lookupTransform', LookupTransform, self.lookupTransform)
        self.srv_ready = rospy.Service('/tf_srv/transformPointCloud', TransformPCL, self.transformPointCloud)

    def lookupTransform(self, req):
        # wait for the transform to be available
        self.listener.waitForTransform(req.source_frame_id, req.target_frame_id, rospy.Time(0), rospy.Duration(10))
        # get the transform
        t, r = self.listener.lookupTransform(req.source_frame_id, req.target_frame_id,rospy.Time(0))
        # define messages to represent translation and rotation
        translation = Vector3(*t)
        rotation = Quaternion(*r)

        return translation, rotation

    def transformPointCloud(self, req):
        # wait for the transform to be available
        self.listener.waitForTransform(
            req.source_frame_id, req.target_frame_id, rospy.Time(0), rospy.Duration(1))
        # transform the input pointcloud to be represented in the source frame
        pcl_out = self.listener.transformPointCloud(req.source_frame_id, req.pcl_in)

        return pcl_out

def main():
    rospy.init_node('tf_srv_node')

    tf_srv = TransformService()

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    main()