import numpy
import random


def makePOS(allLanes, allowedLaneVelocites, maxDist, maxTime,
            initCarX, initCarY):

    spaceFactor = 6

    numLanes = max(allLanes) + 1
    POS = numpy.zeros((numLanes, maxDist, maxTime))

    for ii in range(0, numLanes):

        # generating the spacing for the random other cars
        currLaneVelocityRange = allowedLaneVelocites[ii]
        minAllowedVelInLane = min(currLaneVelocityRange)
        dist = random.randint(0, minAllowedVelInLane * spaceFactor)

        # generating the obstacles for one time slice
        while dist < maxDist:
            POS[ii, dist, 0] = 1
            dist = dist + random.randint(0, minAllowedVelInLane * spaceFactor)

        # make sure to delete any other car that happens to be at the initial
        # state of our car
        POS[initCarX, initCarY, 0] = 0

        # propagating them forward through the time dimesion of the occupancy
        # set
        for time in range(0, maxTime - 1):
            vbuf = (time + 1) * minAllowedVelInLane
            POS[ii, (vbuf + 1):, time + 1] = POS[ii, 1:-vbuf, 0]

    return POS
