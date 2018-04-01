# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 16:01:46 2018

@author: Ahmed Raafat
"""

import random
from random import randint
import re
import itertools





#convert partitioned state into state index for retreiving the reward
def Stateindex(state):
    getnumbers=re.findall('\d+', state)
    values=[]
    
    for i in range (11):
        values.append(int(getnumbers[i]))
    
    output = "".join(map(str, values))
    del values
    return int(output, 2)



def Selectaction(state,table,MaxQIndex,laptime):
    eta=0.1-0.0000003*count()
    egreedy=0.2
    #print("Egreedy= "+ str(eta))
    
    
    Randomnum=random.uniform(0,1)
    if Randomnum< eta:                #Heuristic action
        Action= 0
       # print("Heuristic action")
    elif Randomnum<(eta+float(egreedy)):     #Random action
         Action=1
        # print("Random Action")
    elif Randomnum>(eta+egreedy):     #Qtable action
         Action=2
         #print("Qtable Action")
    
    if Action == 1:
        random_action_index=randint(0,14)
        random_action=ActionTable(random_action_index)
        
        return random_action
    
    elif Action ==2:

        Qtable_Action=ActionTable(MaxQIndex-1)
        
        return Qtable_Action
    else: return ['Hueristic', 'Hueristic']    
    
    

def ActionTable(index):
    if index==0:
        return [1, 0.5]
    elif index==1:
        return [0, 0.5]
    elif index==2:
        return [-1,0.5]
    elif index==3:
        return [1, 0.1]
    elif index==4:
        return [0, 0.1]
    elif index==5:
        return [-1,0.1]
    elif index==6:
        return [1, 0]
    elif index==7:
        return [0, 0]
    elif index==8:
        return [-1,0]
    elif index==9:
        return [1, -0.1]
    elif index==10:
        return [0, -0.1]
    elif index==11:
        return [-1, -0.1]
    elif index==12:
        return [1, -0.5]
    elif index==13:
        return [0, -0.5]
    elif index==14:
        return [-1,-0.5]


def count():
    count.counter += 1 
    return (count.counter)
count.counter = 0
