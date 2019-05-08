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
    def __init__(self, carX, carY, carT, q, prevLane, prevVel):

        self.carX = carX
        self.carY = carY
        self.carT = carT
        self.q = q
        self.prevLane = prevLane
        self.prevVel = prevVel


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
    # @param      observation  A tuple of booleans for the three observations a
    #                          Node in this project can have:
    #                          1) 'atGoal': @bool
    #                          2) 'crashed': @bool
    #                          3) 'speeding': @bool
    # @param      adjList      The Node's adjacency list, containing the
    #                          connected Nodes to this Node instance
    # @param      isAccepting  Indicates if this Node is accepting in a DBA
    # @param      isVisited    Indicates if this Node has been visited during a
    #                          graph search
    #
    def __init__(self, state, index, observation={}, adjList=[],
                 isAccepting=False, isVisited=False):

        self.state = state
        self.index = index
        self.observation = observation
        self.adjList = adjList
        self.isAccepting = isAccepting
        self.isVisited = isVisited
