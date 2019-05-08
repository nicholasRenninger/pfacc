def getSimSettings():

    ########################################################
    # defining road simulation properties
    ########################################################
    allLanes = (1, 2, 3)
    allVelocities = (15, 20, 25, 30, 35)
    allowedLaneVelocites = [(15, 20, 25), (20, 25, 30), (25, 30, 35)]

    ########################################################
    # defining the end of the simulation
    ########################################################

    # pY ranges from 0 - 4000
    maxDist = 4000

    # simulate 100 time steps
    maxTime = 100

    goalX = 1
    goalYMin = 2200
    goalYMax = 2214

    goalStates = makeGoalStates(goalX, goalYMin, goalYMax)

    ########################################################
    # defining the car's initial state
    ########################################################

    # distance from the start of the highway where car starts
    # CANT be 0
    initCarX = 1

    # lane number
    initCarY = 700

    # start the simulation at a time step of 0
    initCarT = 0

    return (allLanes, allVelocities, allowedLaneVelocites, maxDist,
            maxTime, goalStates, initCarX, initCarY, initCarT)


def makeGoalStates(goalX, goalYMin, goalYMax):

    goalStates = []
    for goalY in range(goalYMin, goalYMax + 1):
        goal = (goalX, goalY)
        goalStates.append(goal)

    return goalStates
