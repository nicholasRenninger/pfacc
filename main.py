import OS_Calls
import initialize
import POS
import TransitionSystem


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
                         initCarX, initCarY)

    ########################################################
    # Defining the Transition System
    ########################################################
    TS = TransitionSystem.TransitionSystem(initCarX, initCarY, initCarT,
                                           initCarVel, maxTime, allLanes,
                                           allVelocities, allowedLaneVelocites,
                                           goalStates, POSMat)

if __name__ == "__main__":
    main()
