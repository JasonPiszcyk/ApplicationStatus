#!/usr/bin/env python3
'''
* application_status.py
*
* Copyright (c) 2025 Jason Piszcyk
*
* @author: Jason Piszcyk
* 
* Application Status Info
*
'''
from threading import Lock
import copy
import os


#
# Constants
#


###########################################################################
#
# ApplicationStatus Class
#
###########################################################################
#
# ApplicationConfig
#
class ApplicationStatus():
    ''' Application Status '''
    # Private Class Attributes
    __lock = Lock()
    __lock_env = Lock()
    __conf = {}
    __conf_meta = {}


    #
    # __init__
    #
    def __init__(self, *args, **kwargs):
        ''' Init method for class '''
        super().__init__(*args, **kwargs)



###########################################################################
#
# In case this is run directly rather than imported...
#
###########################################################################
'''
Handle case of being run directly rather than imported
'''
if __name__ == "__main__":
    pass

