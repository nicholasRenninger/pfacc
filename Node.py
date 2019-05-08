class NodeState:
    # @brief      This class (struct) contains all of the info needed to hold
    #             the state of a node in the DFAs used for this project

    #
    # @brief      Constructs the NodeState object.
    #
    # @param      self      The NodeState object instance
    # @param      carX      The current carX value ~ lane on highway
    # @param      carY      The current carY value ~ distance down highway
    # @param      carT      The current carT value ~ current time step
    # @param      q         The LDBA state - pretty much meaningless
    # @param      prevLane  The previous lane for the car during the last time
    #                       step
    # @param      prevVel   The previous velocity for the car during the last
    #                       time step
    #
    def __init__(self, carX, carY, carT, q=None, prevLane=None, prevVel=None):

        self.carX = carX
        self.carY = carY
        self.carT = carT
        self.q = q
        self.prevLane = prevLane
        self.prevVel = prevVel


class Observation:
    # @brief this is just an enum / struct for the three different observations

    #
    # @brief      Constructs the Observation object.
    #
    # @param      self      The Observation object instance
    # @param      atGoal    @bool for inidicating the NodeState is in the goal
    #                       state
    # @param      crashed   @bool for inidicating the NodeState is in a state
    #                       that has collided with an obstacle in the POS
    # @param      speeding  @bool for inidicating the NodeState is such that
    #                       the current velocity exceeds the defined maximum
    #                       allowable velocities
    #
    def __init__(self, atGoal, crashed, speeding):

        self.atGoal = atGoal
        self.crashed = crashed
        self.speeding = speeding


class Node:
    #
    # @brief      Class for a full Node in an automata for this project
    #

    #
    # @brief      Constructs the Node object.
    #
    # @param      self         The Node object instance
    # @param      state        A reference to the NodeState object, containing
    #                          the state info for the node
    # @param      index        The node index (numerical, unique id)
    # @param      obs          An Observation object holding the three
    #                          observations a Node in this project can have:
    #                          1) 'atGoal': @bool
    #                          2) 'crashed': @bool
    #                          3) 'speeding': @bool
    # @param      adjList      The Node's adjacency list, containing the
    #                          connected Nodes to this Node instance
    # @param      isAccepting  Indicates if this Node is accepting in a DBA
    # @param      isVisited    Indicates if this Node has been visited during a
    #                          graph search
    #
    def __init__(self, state, index=None, obs=None, adjList=[],
                 isAccepting=False, isVisited=False):

        self.state = state
        self.index = index
        self.obs = obs
        self.adjList = adjList
        self.isAccepting = isAccepting
        self.isVisited = isVisited
