# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 19:50:44 2022

@author: mrkure
"""

import mouse, time

def lprint():
    print('right')

def mprint():
    print('might')
    
mouse.on_click(lprint)
mouse.on_middle_click(mprint)

time.sleep(10)