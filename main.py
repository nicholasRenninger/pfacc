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

    ########################################################
    # Defining the LTL Deterministic Buchi Automata (LDBA)
    ########################################################
    LTLFormula = 'G(!crashed & !speeding) & F(atGoal)'
    LDBAObj = LDBA.LDBA(LTLFormula)

    ########################################################
    # Creating the Product Automata, using Topological Sort,
    # then backtracking for the solution
    ########################################################
    acceptingGoalNode = DFA.formAndSolveProduct(TS=TS, LDBA=LDBAObj)

    print(acceptingGoalNode)


if __name__ == "__main__":
    main()
