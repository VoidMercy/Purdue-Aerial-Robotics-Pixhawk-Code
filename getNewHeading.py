import math

def getNewHeading(fp, sd, currState, currLoc)

##Define variable for calculations
accel = 9.80655; %m/s
el = currState[1];
dg = currState[4];
yp = fp.wayp(fp.leg);    #is fp a list.  If so, which element is this referencing MATLAB lin. 9
g = getHeading(currLoc, desWayp);  ##What is desired waypoint?
Btwn = getMinAngle(desHdg, currHdg);

##Calculate aircraft turn radius and roll
turnRadius = (currVel  ** 2) / fp.maxGs;
newRoll = atan((currVel ** 2)/ (turnRadius * accel);

##No need to change heading if already on course
if angleBtwn == 0:
	newHdg = currHdg;
	return;

##Calculate heading chagne based on current velocity and turn radius
distToTravel = currVel * sd.timeDelta;
hdgChange = distToTravel / (2*pi*turnRadius) * 360;

##Prevent current heading from overshooting desired heading
if hdgChange > abs(angleBtwn):
    hdgChange = abs(angleBtwn);

##Calculate and return the desired heading
newHdg = currHdg + (angleBtwn / abs(angleBtwn)) * hdgChange;

##TESTING ONLY - Output current function values
##fprintf('currHdg: %0.2f\tdesHdg: %0.2f\tangleBtwn: %0.2f\tnewHdg: 
##0.2f\n', currHdg, desHdg, angleBtwn, newHdg);
