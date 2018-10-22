import random
from math import atan, degrees, pi, radians

def getMinAngle(desHdg, curHdg):
	minAngle = desHdg - curHdg

	if minAngle > 180:
		minAngle -= 360
	elif minAngle < -180:
		minAngle += 360

	return minAngle

def getHeading(loc1, loc2):
	xComp = loc2[0] - loc1[0]
	yComp = loc2[1] - loc1[1]

	if yComp == 0:
		heading = 0
	elif xComp == 0:
		heading = (yComp / abs(yComp)) * 90
	else:
		heading = degrees(atan(radians(yComp / xComp)))

	if xComp < 0:
		heading += 180

	if heading < 0:
		heading += 360
	return heading

def getNewHeading(fp, deltaT, currState, currLoc):
	GRAV_ACCEL = 9.80655
	currVel = currState[0]
	currHdg = currState[3]
	desWayp = fp.wayp[fp.leg]
	desHdg = getHeading(currLoc, desWayp)
	angleBtwn = getMinAngle(desHdg, currHdg)
	
	#Calculate aircraft turn radius and roll
	turnRadius = currVel ** 2 / float(fp.maxGs)
	newRoll = degrees(atan(radians(currVel ** 2 / (turnRadius * GRAV_ACCEL))))
	
	if angleBtwn == 0:
		newHdg = currHdg
		
	distToTravel = currVel * deltaT
	hdgChange = distToTravel / (2 * pi * turnRadius) * 360
	
	if hdgChange > abs(angleBtwn):
		hdgChange = abs(angleBtwn)
	
	newHdg = currHdg + (angleBtwn / abs(angleBtwn)) * hdgChange
	
	return newHdg, newRoll
	
	
