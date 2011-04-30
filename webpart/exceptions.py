# -*- coding: utf-8 -*-
'''
Created on 09.04.2011

@author: WQ85KUH

Exceptions for package
'''
        
class UserOfflineError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
