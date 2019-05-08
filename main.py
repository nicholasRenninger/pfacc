import OS_Calls
import initialize
import POS


def main():

    OS_Calls.clear_screen()

    ########################################################
    # defining simulation properties
    ########################################################

    (allLanes, allVelocities,
     allowedLaneVelocites, maxDist,
     maxTime, goalStates, initCarX,
     initCarY, initCarT, initCarVel) = initialize.getSimSettings()

    ########################################################
    # Defining the Occupancy Set
    ########################################################

    POSMat = POS.makePOS(allLanes, allowedLaneVelocites,
                         maxDist, maxTime,
                         initCarX, initCarY, initCarVel)

    ########################################################
    # Defining the Transition System
    ########################################################


if __name__ == "__main__":
    main()
