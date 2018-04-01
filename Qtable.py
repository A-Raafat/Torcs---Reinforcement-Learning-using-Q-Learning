# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 18:36:08 2018

@author: Ahmed Raafat
"""
import itertools
import pandas as pd
import numpy
import re

learning_rate=0.01
Discount=0.99
i=1

def maketable():        #Makes the Qtable consisting of 11 combinations with partitions for readability in a dataframe
    Statestring=[]       #Empty list to append the state partitions
    States= list(itertools.product([0,1], repeat=11))
    for i in range (2048):     #Partitioning the states for readability
        x1=States[i][0:4]
        x2=States[i][4:7]
        x3=States[i][7:11]

        Statestring.append(str(x1)+str(x2)+str(x3)) #Transforming the partitions into strings
    data= numpy.c_[Statestring,numpy.zeros((2048,15)) ]
    s=pd.DataFrame(data)   #Creating the Qtable s
    return s


def update(state,Actionindex,Next_Qmax,NextState,Current_Reward,qtable): #Writes in the Qtable given Accelerate+Steer, gear and meta values
   # z=count()
    #print("Update number: "+str(z))
   # if z>=750000:
        #print("STOP")
    Statestring=convert2string(state)#Converts the state into partitioned one to index the Qtable of partitioned states
    Current_Q=float(qtable.loc[Stateindex(Statestring)][Actionindex+1])   #Add +1 after first iteration
    NQmax=float(qtable.loc[Stateindex(convert2string(NextState))][Next_Qmax])
    #print("Action index= "+str(Actionindex)+"Current_Q="+str(Current_Q)+" Current_Reward="+str(Current_Reward)+" NextQmax= "+str(NQmax))
    qtable.iloc[Stateindex(Statestring),Actionindex+1]=Current_Q+learning_rate*(Current_Reward+Discount*NQmax-Current_Q)  #updates the Qtable   
    

def convert2string(state):     #Converting state into partioned state (0000)(000)(0000)
    b=tuple(state)
    x=str(b[0:4])+str(b[4:7])+str(b[7:11])
    return x


def count():
    count.counter += 1 
    return(count.counter)
count.counter = 0


def Stateindex(state):
    getnumbers=re.findall('\d+', state)
    values=[]
    
    for i in range (11):
        values.append(int(getnumbers[i]))
    
    output = "".join(map(str, values))
    del values
    return int(output, 2)