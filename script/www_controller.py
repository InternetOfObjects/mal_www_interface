#!/usr/bin/env python

import rospy

from mal_www_interface import WWWController

if __name__ == '__main__':
    try:
        node = WWWController()
        node.main()
    except rospy.ROSInterruptException:
        pass
