import OS_Calls
import initialize
import POS
import TransitionSystem
import LDBA
import DFA


def main():

    OS_Calls.clear_screen()

    ########################################################
    # defining simulation properties
    ########################################################

    (allLanes, allVelocities,
     allowedLaneVelocites, maxDist,
     maxTime, goalStates, initCarX,
     initCarY, initCarT, initCarVel) = initialize.getSimSettings()

    print('defined simulation properties')

    ########################################################
    # Defining the Occupancy Set
    ########################################################

    POSMat = POS.makePOS(allLanes, allowedLaneVelocites,
                         maxDist, maxTime,
                         initCarX, initCarY)

    print('built the occupancy set')

    ########################################################
    # Defining the Transition System
    ########################################################

    print('building the transition system...')

    TS = TransitionSystem.TransitionSystem(initCarX, initCarY, initCarT,
                                           initCarVel, maxTime, allLanes,
                                           allVelocities, allowedLaneVelocites,
                                           goalStates, POSMat)

    print('built the transition system')

    ########################################################
    # Defining the LTL Deterministic Buchi Automata (LDBA)
    #######################################################

    LTLFormula = 'G(!crashed & !speeding) & F(atGoal)'
    LDBAObj = LDBA.LDBA(LTLFormula)

    print('built the LDBA')

    ########################################################
    # Creating the Product Automata, using Topological Sort,
    # then backtracking for the solution
    ########################################################

    print('calculating the product automata')

    acceptingGoalNode = DFA.formAndSolveProduct(TS=TS, LDBA=LDBAObj)

    print('found the final solution node in the product')

    print(acceptingGoalNode)


if __name__ == "__main__":
    main()
