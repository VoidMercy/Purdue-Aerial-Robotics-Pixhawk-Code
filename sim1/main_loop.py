import random, math
from update_position import updateACPos
from get_heading import getNewHeading
from get_pitch import getNewPitch
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

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

def getNewACState(fp, curState, curLoc, deltaT):
    newHdg, newRoll = getNewHeading(fp, deltaT, curState, curLoc)
    newPitch = getNewPitch(fp, deltaT, curState, curLoc)
    newVel = curState[0]
    newState = [newVel, newRoll, newPitch, newHdg]
    newLoc = updateACPos(curLoc, newState, deltaT)
    return newState, newLoc

def generateRandomWaypoints():
    list_of_waypoints = []
    for i in range(4):
        #north, east, alt
        tmp = [random.randint(800, 1000), random.randint(800, 1000), random.randint(800, 1000)]
        list_of_waypoints.append(tmp)
    return list_of_waypoints

temp = fp()
temp.north = [0, 100, 100, 0]
temp.east = [0, 100, 100, 0]
temp.alt = [0, 100, 50, 0]
temp.vel = [20, 20, 20, 20]
temp.rph = [0, 0, 0]
#temp.wayp = generateRandomWaypoints()
for i in range(4):
    temp.wayp.append([temp.north[i], temp.east[i], temp.alt[i]])
print temp.wayp
temp.leg = 1
temp.maxGs = 50
temp.successRadius = 5

deltaT = 0.05
curState = [temp.vel[temp.leg], temp.rph[0], temp.rph[1], temp.rph[2]] #velocity, roll, pitch, heading
curWayp = temp.wayp[temp.leg]
curLoc = [0, 0, 0] #posX, posY, alt
c = 0

print "Starting Location: " + str(curLoc)
print "Waypoints: " + str(temp.wayp)

#plotting stuff
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xs, ys, zs = [], [], []
ax.scatter(curLoc[0], curLoc[1], curLoc[2], c=(0, 1, 0))

while c < 100:
    #determine if the desired waypoint has been reached
    if calcDist3D(curLoc, curWayp) <= temp.successRadius:
        #yay we're within the waypoint
        print "REACHED: " + str(curWayp)
        temp.leg += 1

        if temp.leg >= len(temp.wayp):
            #reached all waypoints
            print "DONE"
            break

        #update waypoint
        curWayp = temp.wayp[temp.leg]
    #print curLoc
    #print curState
    #calculate new state
    curState, curLoc = getNewACState(temp, curState, curLoc, deltaT)
    xs.append(curLoc[0])
    ys.append(curLoc[1])
    zs.append(curLoc[2])
    #print curLoc
    c += deltaT

ax.set_xlabel('X Pos')
ax.set_ylabel('Y Pos')
ax.set_zlabel('Altitude')

for i in temp.wayp:
    ax.scatter([i[0]], [i[1]], [i[2]], c=(1, 0, 0))

ax.scatter(xs, ys, zs)

plt.show()