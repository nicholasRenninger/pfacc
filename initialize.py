def getSimSettings():

    ########################################################
    # defining road simulation properties
    ########################################################
    allLanes = (0, 1, 2)
    allVelocities = (30, 40, 50, 60, 70)
    allowedLaneVelocites = [(30, 40, 50), (40, 50, 60), (50, 60, 70)]

    ########################################################
    # defining the end of the simulation
    ########################################################

    # pY ranges from 0 - 4000
    maxDist = 600

    # simulate maxTime time steps
    maxTime = 20

    goalX = 0
    goalYMin = 400
    goalYMax = 500

    goalStates = makeGoalStates(goalX, goalYMin, goalYMax)

    ########################################################
    # defining the car's initial state
    ########################################################

    # distance from the start of the highway where car starts
    # CANT be 0
    initCarX = 0

    # lane number
    initCarY = 150

    # start the simulation at a time step of 0
    initCarT = 0

    # need to be safe and set some sort of min velocity
    initCarVel = min(allowedLaneVelocites[initCarX])

    return (allLanes, allVelocities, allowedLaneVelocites, maxDist,
            maxTime, goalStates, initCarX, initCarY, initCarT, initCarVel)


def makeGoalStates(goalX, goalYMin, goalYMax):

    goalStates = []
    for goalY in range(goalYMin, goalYMax + 1):
        goal = (goalX, goalY)
        goalStates.append(goal)

    return goalStates
