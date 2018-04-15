'''
Created on Apr 4, 2012

@author: lanquarden 

Edited by: Ahmed Raafat
'''

import msgParser
import carState
import carControl
import GetState2
import Qtable
import GetAccSteer
import math
import ActionSelection
import RewardFunction
import pandas
import time

staaart=0

Current_State=None
Taken_ActionIndex=None
Reward=None

class Driver(object):
    '''
    A driver object for the SCRC
    '''
   

    def __init__(self, stage):
        '''Constructor'''
        self.WARM_UP = 0
        self.QUALIFYING = 1
        self.RACE = 2
        self.UNKNOWN = 3
        self.stage = stage
        
        self.parser = msgParser.MsgParser()
        
        self.state = carState.CarState()
        
        self.control = carControl.CarControl()
        
        self.steer_lock = 0.785398
        self.max_speed = 160
        self.prev_rpm = None
        #self.table=Qtable.maketable()
        #after first iteration
        self.table=pandas.read_csv("../input_path/Qtable.csv")
        
        self.Accelerate=0
        self.Gearshift=0
        self.steerval=0
        
        
        
    
    def init(self):
        '''Return init string with rangefinder angles'''
        self.angles = [0 for x in range(19)]
        
        for i in range(5):
            self.angles[i] = -90 + i * 15
            self.angles[18 - i] = 90 - i * 15
        
        for i in range(5, 9):
            self.angles[i] = -20 + (i-5) * 5
            self.angles[18 - i] = 20 - (i-5) * 5
        
        return self.parser.stringify({'init': self.angles})
    
    def drive(self, msg):
        start=time.time()
        DistanceNOW=self.state.getDistRaced()
        #print("DISTANCEEE="+str(DistanceNOW))
        self.state.setFromMsg(msg)
        
        global staaart
        track    = self.state.getTrack()    #Stores the 19 sensors in track variable
        speed    = self.state.getSpeedX()   #Stores the speed value 
        trackpos = self.state.getTrackPos()
        angle    = self.state.getAngle()
              
        state=GetState2.State(speed,track,trackpos) #Gets the state partitioned form

        if staaart==0:
            #Current state
            staaart+=1
            
            global Current_State
            global Taken_ActionIndex
            global Reward
            Current_State=state
            
            Qmax_current=RewardFunction.FindQmaxIndex(Current_State,self.table)
            speedselect, steerselect=ActionSelection.Selectaction(Current_State,self.table, Qmax_current,self.state.getCurLapTime()) #Action Selection
            Reward=0
            Reward_Next=0
       
            if speedselect=='Hueristic':
                SteerValue=self.steer()          #Storing stear value
                self.gear()
                AccelValue=self.speed()
            else:
                self.control.setSteer(steerselect)
                self.gear()
                self.control.setAccel(speedselect)
                SteerValue=steerselect
                AccelValue=speedselect
            
            Taken_ActionIndex=GetAccSteer.AccelSteer(AccelValue,SteerValue) #Takes the action taken in current state and encodes it
        
        else:
                                         
            Next_State=state
            Qmax_Next=RewardFunction.FindQmaxIndex(Next_State,self.table)
            Reward_Next=RewardFunction.ComputeReward(speed,trackpos,angle,DistanceNOW)
            speedselect, steerselect=ActionSelection.Selectaction(Next_State,self.table, Qmax_Next,self.state.getCurLapTime()) #Action Selection
            if speedselect=='Hueristic':
                SteerValue=self.steer()          #Storing stear value
                self.gear()
                AccelValue=self.speed()
            else:
                self.control.setSteer(steerselect)
                self.gear()
                self.control.setAccel(speedselect)
                SteerValue=steerselect
                AccelValue=speedselect
            
            Next_Taken_ActionIndex=GetAccSteer.AccelSteer(AccelValue,SteerValue) #Takes the action taken in current state and encodes it
            
        
        
            Qtable.update(Current_State,Taken_ActionIndex,Qmax_Next,Next_State,Reward_Next,self.table)      #Writes the action in cur
            
            #print("CURRENT STATE = "+str(Current_State) + "  NEXT STATE = " + str(Next_State))
            Current_State=Next_State
            Taken_ActionIndex=Next_Taken_ActionIndex
            
        

           
        if Reward_Next==-2 or self.state.getDamage() > 8500 :
            self.control.setMeta(1)
        #2print("TIME TAKEN= " + str(time.time()-start))
        
        return self.control.toMsg()
    
    
    def steer(self):
        angle = self.state.angle
        dist = self.state.trackPos
        
        
        go=(angle - dist*0.5)/self.steer_lock
        self.control.setSteer(go)  #heuristic
    
        return go
        
    def gear(self):
        gearup   =[7000 , 7000 , 7000 , 7000 , 7000 , 0]
        geardown =[0 , 2500 , 3000 , 3000 , 3500 , 3500]
        gear = self.state.getGear()
        rpm = self.state.getRpm()
        if gear < 1 :
            gear = 1 
        if(gear < 6) and (rpm  >= gearup[gear -1]):
            gear = gear +1 ;
        elif(gear > 1) and (rpm <= geardown[gear -1]):
            gear =  gear -1
        else:
            gear = gear
        self.control.setGear(gear)
    
    def speed(self):
        maxSpeedDist=70
        maxSpeed=self.max_speed
        
        track=self.state.getTrack()
        Right=track[13]
        Left=track[5]
        Center=track[9]
        
        if (Center>maxSpeedDist) or (Center>=Right and Center>=Left):
            targetSpeed=maxSpeed
        else:
            if Right>Left:
                h=Center*math.sin(5)
                b=Right-Center*math.cos(5)
                sinAngle=b*b/(h*h+b*b)
                
                targetSpeed=maxSpeed*(Center*sinAngle/maxSpeedDist)
            else:
                h=Center*math.sin(5)
                b=Left-Center*math.cos(5)
                sinAngle=b*b/(h*h+b*b)
                
                targetSpeed=maxSpeed*(Center*sinAngle/maxSpeedDist) 
        accel=2/(1+math.exp(self.state.getSpeedX()-targetSpeed))-1
        self.control.setAccel(accel)
        return accel
            
        
    def onShutDown(self):
        pass
    
    def onRestart(self):
        pass
        
