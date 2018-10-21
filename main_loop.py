import random, math
from update_position import updateACPos

class fp(object):
    def __init__(self, north=None, east=None, alt=None, vel=None, leg=None, maxGs=None, rph=None, successRadius=None, wayp=None):
        self.north = north
        self.east = east
        self.alt = alt
        self.vel = vel
        self.leg = leg
        self.maxGs = maxGs
        self.rph = rph
        self.successRadius = successRadius
        self.wayp = []

def calcDist3D(curLoc, curWayp):
    return math.sqrt((curLoc[0] - curWayp[0])**2 + (curLoc[1] - curWayp[1]) ** 2 + (curLoc[2] - curWayp[2]) ** 2)

def getNewHeading(fp, curState, curLoc):
    return 0

def getNewPitch(fp, curState, curLoc):
    return 0

def getNewACState(fp, curState, curLoc, deltaT):
    newHdg, newRoll = getNewHeading(fp, curState, curLoc)
    newPitch = getNewPitch(fp, curState, curLoc)
    newVel = curState[1]
    newState = [newVel, newRoll, newPitch, newHdg]
    newLoc = updateACPos(curLoc, newState, deltaT)
    return newState, newLoc

def generateRandomWaypoints():
    list_of_waypoints = []
    for i in range(4):
        #north, east, alt
        tmp = [random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)]
        list_of_waypoints.append(tmp)
    return list_of_waypoints

temp = fp()
temp.north = [0, 0, 100, 0]
temp.east = [0, 100, 100, 0]
temp.alt = [0, 100, 50, 0]
temp.vel = [20, 20, 20, 20]
temp.rph = [1, 1, 1]
temp.wayp = generateRandomWaypoints()
temp.leg = 0
temp.maxGs = 50
temp.successRadius = 5

iteration_num = 100
deltaT = 0.1

curState = [0, 0, 0, 0] #velocity, roll, pitch, heading
curWayp = temp.wayp[0]
curLoc = [0, 0, 0] #posX, posY, alt
c = 0

while c < iteration_num:

    #determine if the desired waypoint has been reached
    if calcDist3D(curLoc, curWayp) <= temp.successRadius:
        #yay we're within the waypoint
        temp.leg += 1

        if temp.leg > len(temp.wayp):
            #reached all waypoints
            print "DONE"
            exit()

        #update waypoint
        curWayp = temp.wayp[temp.leg]

    #calculate new state
    curState, curLoc = getNewACState(temp, curState, curLoc, deltaT)
