from math import cos, sin, radians, degrees, sqrt, atan2, atan
import random, numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def generateRandomWaypoints(num):
    list_of_waypoints = []
    for i in range(num):
        #north, east, alt
        tmp = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
        list_of_waypoints.append(tmp)
    return list_of_waypoints

def calcDistance3D(a, b):
	return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

def calcDistance2D(a, b):
	return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def changePlaneDir(loc, prevWayp, desWayp, method):
	delta = 3
	perpCoord = calculateIntercepts(loc, prevWayp, desWayp)
	lookaheadDistDirect = calcDistance2D(desWayp, perpCoord)
	thetaPath = atan2(desWayp[1] - perpCoord[1], desWayp[0] - perpCoord[0])
	crosstrack = sin(atan2(perpCoord[1] - loc[1], perpCoord[0] - loc[0]) - thetaPath) * calcDistance2D(perpCoord, loc)

	if method == 1:
		thetaError = atan(crosstrack / lookaheadDistDirect)
	else:
		thetaError = atan(crosstrack / delta)

	desiredDir = 90 - degrees(thetaPath - thetaError)
	return desiredDir

def changePlanePitch(loc, desWayp, currPitch):
	maxPitchChange = 5
	maxPitch = 30
	pitch = degrees(atan2(desWayp[2] - loc[2], calcDistance2D(loc, desWayp)))

	if pitch - currPitch > maxPitchChange:
		pitch = currPitch + maxPitchChange
	elif pitch - currPitch < -maxPitchChange:
		pitch = currPitch - maxPitchChange

	if pitch > maxPitch:
		pitch = maxPitch
	elif pitch < -maxPitch:
		pitch = -maxPitch
	return pitch

def calculateIntercepts(loc, prevWayp, desWayp):
	if desWayp[1] - prevWayp[1] != 0 and desWayp[0] - prevWayp[0] != 0:
		slope = (desWayp[1] - prevWayp[1]) / float(desWayp[0] - prevWayp[0])
		yInt = desWayp[1] - slope * desWayp[0]

		crossTrackInt = loc[1] + loc[0] / slope

		xIntDirect = (yInt - crossTrackInt) / ((-1.0 / slope) - slope)
		yIntDirect = (-1.0 / slope) * xIntDirect + crossTrackInt
		perpCoord = [xIntDirect, yIntDirect]
	elif desWayp[1] - prevWayp[1] == 0:
		perpCoord = [loc[0], desWayp[1]]
	elif desWayp[0] - prevWayp[0] == 0:
		perpCoord = [desWayp[0], loc[1]]

	return perpCoord

def isReachable(loc, prevWayp, currWayp, currDir):
	turnRadius = 10.0
	successRadius = 4.0
	distToWayp = calcDistance2D(currWayp, loc)
	if distToWayp >= turnRadius - 0.75 * successRadius or distToWayp <= successRadius:
		return True
	else:
		angleToTarget = changePlaneDir(loc, prevWayp, currWayp, 1)
		if abs(angleToTarget - currDir) < 55:
			return True
		else:
			return False
numIter = 2000
loc = [0, 0, 0] #initial location
wayp = generateRandomWaypoints(5)
planeDir = 90
planePitch = 0
planeSpeed = 1
turnRadius = 10
successRadius = 4
windspeed = [0, 0, 0]
iteration = 0
currWaypNum = 0
locationArray = [[0, 0, 0]] * numIter
hitTargetArray = []
for i in wayp:
	hitTargetArray.append(i[:])
currWayp = wayp[currWaypNum]
prevWayp = loc

#PLOTTING STUFF
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xs, ys, zs = [], [], []
ax.scatter(loc[0], loc[1], loc[2], c=(0, 1, 0))
print wayp


while iteration < numIter and currWaypNum < len(wayp):
	#store and update current position
	locationArray[iteration][0] = loc[0]
	locationArray[iteration][1] = loc[1]
	locationArray[iteration][2] = loc[2]
	loc[0] = loc[0] + windspeed[0] + planeSpeed * cos(radians(90 - planeDir))
	loc[1] = loc[1] + windspeed[1] + planeSpeed * sin(radians(90 - planeDir))
	loc[2] = loc[2] + windspeed[2] + planeSpeed * sin(radians(planePitch))
	xs.append(loc[0])
	ys.append(loc[1])
	zs.append(loc[2])

	#update desired heading
	desiredDir = changePlaneDir(loc, prevWayp, currWayp, 1)
	planePitch = changePlanePitch(loc, currWayp, planePitch)

	planeDir = planeDir % 360.0
	if planeDir < 0:
		planeDir += 360
	if desiredDir < 0:
		desiredDir += 360

	#eliminate roll-over error (always turn in shortest direction)
	if desiredDir - planeDir > 180:
		desiredDir -= 360
	elif desiredDir - planeDir < -180:
		desiredDir += 360

	#limit plane's turning ability
	if planeDir - desiredDir > turnRadius:
		planeDir -= turnRadius
	elif planeDir - desiredDir < -turnRadius:
		planeDir = planeDir + turnRadius
	else:
		planeDir = desiredDir

	#calculate the distance between the plane and its destionation
	distanceToWayp = calcDistance3D(loc, currWayp)

	#check if the plane has reached its destination
	if distanceToWayp < successRadius:
		print "REACHED SMTH"
		#hitTargetArray[iteration][0] = loc[0]
		#hitTargetArray[iteration][1] = loc[1]
		#hitTargetArray[iteration][2] = loc[2]

		prevWay = currWayp
		currWaypNum += 1
		if currWaypNum < len(wayp):
			currWayp = wayp[currWaypNum]
		else:
			print "DONE"
			break

		reachable = isReachable(loc, prevWayp, currWayp, planeDir)

		if not reachable:
			print "NOT REACHABLE"

		while not reachable:
			loc[0] = loc[0] + windspeed[0] + planeSpeed * cos(radians(90 - planeDir))
			loc[1] = loc[1] + windspeed[1] + planeSpeed * sin(radians(90 - planeDir))
			loc[2] = loc[2] + windspeed[2] + planeSpeed * sin(radians(planePitch))
			reachable = isReachable(loc, prevWayp, currWayp, planeDir)

	iteration += 1

if currWaypNum < len(wayp):
	print "NOT ALL WAYPOINTS REACHED"

#now plot stuff
ax.set_xlabel('X Pos')
ax.set_ylabel('Y Pos')
ax.set_zlabel('Altitude')

ax.scatter(xs, ys, zs)

for i in wayp:
    ax.scatter(i[0], i[1], i[2], c=(1, 0, 0))

plt.show()