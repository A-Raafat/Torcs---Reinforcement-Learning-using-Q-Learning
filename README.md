# Torcs - Reinforcement-Learning
Discretized Q-Learning on Torcs ( Lane keeping assistant )

## Introduction
**The Open Racing Car Simulator.** TORCS is a modern, modular, highly-portable multi-player, multi-agent car simulator. Its high degree of modularity and portability render it ideal for artificial intelligence research.
 
TORCS can be used to develop artificially intelligent (AI) agents for a variety of problems. At the car level, new simulation modules can be developed, which include intelligent control systems for various car components. At the driver level, a low-level Application program interface (API) gives detailed (but only partial) access to the simulation state. This could be used to develop anything from mid-level control systems to complex driving agents that find optimal racing lines, react successfully in unexpected situations and make good tactical race decisions.
Each on-going race is referred to as a simulation in TORCS and is described through many different data structures. The race situation is updated every 2 milliseconds (500 Hz), including updating the various mathematical models governing the physics of the race, e.g. motion and positioning of the cars and other objects.

You can download TORCS from this link:
[TORCS](http://torcs.sourceforge.net/index.php?name=Sections&op=viewarticle&artid=3)

## SCR-Plugin


<p align="center">
  <img width="460" height="300" src="https://github.com/A-Raafat/Torcs---Reinforcement-Learning/blob/master/Pic.png">
</p>

## TORCS Sensors 
| Sensor | Definition |
| ------ | ---------- |
| Angle |  Angle between the car direction and the direction of the track axis |
| CurLapTime | Time elapsed during current lap |
| Damage | Current damage of the car (the higher is the value the higher is the damage) |
| distFromStartLine | Distance of the car from the start line along the track line |
| Distracted | Distance covered by the car from the beginning of the race |
| Fuel | Current fuel level |
| Gear | Current gear: -1 is reverse 0 is neutral and the gear from 1 to 6 |
| lastLapTime |  Time to complete last lap. Opponents: Vector of 36 sensors that detects the opponent distance in meters (range is [0,100]) within a specific 10 degrees sector: each sensor covers 10 degrees, from  -π to +π  around the car |
| racePos | Position in the race with respect to other cars |
| rpm | Number of rotations per minute of the car engine |
| speedX | Speed of the car along the longitudinal axis of the car |
| speedY | Speed of the car along the transverse axis of the car |
| track | Vector of 19 range finder sensors: each sensor represents the distance between the track edge and the car. Sensors are oriented every 10 degrees from -π/2 and +π/2 in front of the car. Distance are in meters within a range of 100 meters. When the car is outside of the track (i.e. track Pos is less than -1 or greater than 1), these values are not reliable! |
| trackPos | Distance between the car and the track axis. The value is normalized w.r.t. the track width: it is 0 when the car is on the axis, -1 when the car is on the left edge of the track and +1 when it is on the right edge of the car. Values greater than 1 or smaller than -1 means that the car is outside of the track |
| wheelSpinVel |  Vector of 4 sensors representing the rotation speed of the wheels |

# TORCS Control Actions
Accel: Virtual gas pedal (0 means no gas, 1 full gas).

Brake: Virtual brake pedal (0 means no brake, 1 full brake).

Gear: Gear value

Steering: Steering value: -1 and +1 means respectively full left and right, that corresponds to an angle of 0.785398 rad.

Meta: This is meta-control command: 0 Do nothing, 1 ask competition server to restart the race.


# Procedure

1- STATES

it’s clear that most of the sensor readings represent car states and it is very important for control the car

The states are the speed along the track, the position on the track, the angle with respect to the track axis and five distance sensors that measure the distance to the edge of the track. Note that the track may contain a gravel trap or a bank of grass, which means that the edge of the track might be further away than the edge of the actual road. The 20◦ inputs are not taken directly from sensors 7 and 11, but computed as an average over sensors 6, 7, 8 and 10, 11, 12, respectively, to account for noise






Sensor name	State Description
Speed X	Speed of the car along the longitudinal axis of the car
Angle	Angle between the car direction and the direction of the track axis.
Track pos	Distance between the car and the track axis
Distance sensor at −40◦, −20◦, 0◦, 20◦, 40◦	Distance between the car and track [5, 7, 9, 11, 13]



2-Actions

There are five action dimensions available in TORCS accelerate, brake, gear, meta and steer. Since braking is simply a negative acceleration, we shall view this as the negative side of the same dimension.

The basic controller of the SCR
Name	Range	Description
Accel	[0,1]	Virtual gas pedal (0 means no gas, 1 full gas).
Brake	[0,1]	Virtual brake pedal (0 means no brake, 1 full brake)
Gear	-1,0,1,2,3,4,5,6	Gear value.
Steer	[-1,1]	Steering value: -1 and +1 means respectively full right and left
Meta	0 or 1	This is meta-control command: 0 do nothing, 1 ask competition server to restart the race





Gear:
shifts gear according to the rpm of the car’s engine in Gear shifting values table

Gear	         1	         2   	          3	         4	         5	        6
Shift up	8000	 9500	9500	9500	9500	0
Shift down	0	4000	6300	7000	7300	7300

Steer:
 we should make a discretization of these dimensions is needed. Initially the agent was given seven steering actions: -1, -0.5, -0.1, 0, 0.1, 0.5, and 1. This includes actions for small deviations and actions with a larger impact to pass sharp curves, but to provide sharp edges we remove (-1) and (1)

Accel:
The values for acceleration were tuned manually as well. Since human players tend to balance between full acceleration and no acceleration at all and since the time resolution is quite high (one action per 20ms), it seemed unnecessary to give the agent a high resolution in the acceleration dimension. The agent was given three values: 1, 0 and -1,

actually, steering correlated with acceleration and brake so the resulting discretization give us the following combinations

3-Rewards

Due to random actions there are good actions and bad actions, we want to achieve our target so we want to prevent the car to
1-going out of the track
2-stopping in a certain position
3-making bad actions

to calculate the rewards, we have 3 situations:

1- car make good lane keeping
the reward will be positive and high if the distance was long and in general it has a continuous range from [-1,1]

2-stop in certain position
the reward will be negative and equal to -1

3- the car goes out of the track
the reward will be negative and equal to -1 and we will restart the race
