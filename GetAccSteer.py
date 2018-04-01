# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 21:24:19 2018

@author: Ahmed Raafat
"""
def DiscSteer(steer):           #Discretizing Steering value
    if   steer>=0.33                 : Dsteer=0.5
    elif steer< 0.33 and steer>0.02  : Dsteer=0.1
    elif steer<=0.02 and steer>=-0.02: Dsteer=0
    elif steer<-0.02 and steer>-0.33 : Dsteer=-0.1
    elif steer<=-0.33                : Dsteer=-0.5

    return Dsteer

def DiscAccel(accel):
    if accel>=0.33                   : Daccel=1
    elif accel<0.33 and accel>=-0.33 : Daccel=0
    elif accel<-0.33                 : Daccel=-1
    return Daccel

def AccelSteer(accel,steer):      #Encoding Accelerate + Steer in one partition
    S=DiscSteer(steer)
    A=DiscAccel(accel)
    
    if A==1:
        if   S==0.5  : Actionindex=0
        elif S==0.1  : Actionindex=3
        elif S==0    : Actionindex=6
        elif S==-0.1 : Actionindex=9
        elif S==-0.5 : Actionindex=12
    elif A==0:
        if   S==0.5  : Actionindex=1
        elif S==0.1  : Actionindex=4
        elif S==0    : Actionindex=7
        elif S==-0.1 : Actionindex=10
        elif S==-0.5 : Actionindex=13
    elif A==-1:
        if   S==0.5  : Actionindex=2
        elif S==0.1  : Actionindex=5
        elif S==0    : Actionindex=8
        elif S==-0.1 : Actionindex=11
        elif S==-0.5 : Actionindex=14
        
    
    return Actionindex
