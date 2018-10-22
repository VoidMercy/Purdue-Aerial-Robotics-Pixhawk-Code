import math 

# updateACPos Calculates and returns the new location of the aircraft based
# on its velocity, orientation, and current location.
def updateACPos(currLoc, currState, timeDelta):
     
    # Define variables for calculations
    currVel = currState[0]
    currPitch = 90 - currState[2]
    currHdg = currState[3]

    newPos = currLoc[:]
    
    # Calculate the unit vector pointing in the direction defined by the
    # current heading and current pitch
    dirVec = [math.sin(math.radians(currPitch)) * math.cos(math.radians(currHdg)), math.sin(math.radians(currPitch)) * math.sin(math.radians(currHdg)), math.cos(math.radians(currPitch))]
    
    #Update current AC position
    for i in range(len(dirVec)):
        dirVec[i] = math.degrees(dirVec[i])
        newPos[i] += dirVec[i] * currVel * timeDelta

    return newPos