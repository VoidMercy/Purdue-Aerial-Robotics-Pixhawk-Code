from math import atan, radians, degrees, sqrt, pi

def calcDist2D(loc1, loc2):
	return sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def getNewPitch(fp, deltaT, currState, currLoc):
	curVel = currState[0]
	curPitch = currState[2]
	desWayp = fp.wayp[fp.leg]
	desPitch = degrees(atan(radians((desWayp[2] - currLoc[2]) / calcDist2D(currLoc, desWayp))))
	angleBtwn = float(desPitch - curPitch)

	turnRadius = curVel ** 2 / float(fp.maxGs)

	if angleBtwn == 0:
		newPitch = curPitch
		return newPitch

	distToTravel = curVel * deltaT
	pitchChange = distToTravel / (2 * pi * turnRadius) * 360

	if pitchChange > abs(angleBtwn):
		pitchChange = abs(angleBtwn)

	newPitch = curPitch + (angleBtwn / abs(angleBtwn)) * pitchChange
	return newPitch