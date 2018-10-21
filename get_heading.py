import random

def getHeading(fp, deltaT, currState, currLoc):
	GRAV_ACCEL = 9.80655
	currVel = currState[1]
	Hdg = currState[1]
	desWayp = fp.wayp(fp.leg, a[:])
	angleBtwn = getMinAngle(desHdg,currHdg)
	
	#Calculate aircraft turn radius and roll
	turnRadius = currVel ** 2 / fp.maxGs
	newRoll = atand(curVel ** 2 / (turnRadius * GRAV_ACCEL))
	
	if (angleBtwn == 0):
		newHdg = currHdg
		
	distToTravel = currVel * sd.timeDelta
	hdgChange = distToTravel / (2 * pi * turnRadius) * 360
	
	if (hdgChange > abs(angleBtwn)):
		hdgChange = abs(angleBtwn)
	
	newHdg = currHdg + (angleBtwn / abs(angleBtwn)) * hdgChange:
	
	
	
	
	
