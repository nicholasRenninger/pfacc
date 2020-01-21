from __future__ import print_function
import Node
from collections import deque


class DFA:
    # @brief      A class representing a Deterministic Finite Automata

    # @brief      Constructs the DFA object.
    #
    # @param      self       The object instance reference
    # @param      nodes      A list of Node objects making up the DFA
    # @param      startNode  The initializing Node object
    # @param      transFcn   The transaction function for the DFA
    # @param      accepts    A list of indices into nodes for Nodes that accept
    #
    def __init__(self, nodes, startNode, transFcn=None, accepts=None):

        self.nodes = nodes
        self.startNode = startNode
        self.transFcn = transFcn
        self.accepts = accepts


#
# @brief      This functions forms the product automata between a deterministic
#             Buchi automata and a deterministic finite transition
#             system.transition
#
#             As forming the product involves using a graph search (here the
#             graph search is based on BFS), we simply instrument this BFS
#             search to build up a path through the product, and return once it
#             finds the first accepting state. As this graph is a DAG, BFS
#             produces the shortest path through the graph and thus this trace
#             in the product is actually the optimal controller.
#
# @param      DTS    A TransistionSystem to product with the LBDA, containing
#                    the physical modeling transitions
# @param      LDBA   The LDBA (LTL Deterministic Buchi Automata) encoding the
#                    LTL specification on DTS
#
# @return     the first Node object in the product to accept
#
def formAndSolveProduct(DTS, LDBA):

    startTSNode = DTS.DFA.startNode
    startLDBANode = LDBA.DFA.startNode

    startTSState = startTSNode.state
    carX = startTSState.carX
    carY = startTSState.carY
    carT = startTSState.carT
    prevLane = startTSState.prevLane
    prevVel = startTSState.prevVel
    obs = startTSNode.obs

    q = startLDBANode.state.q

    startProdState = Node.NodeState(carX, carY, carT, q, prevLane, prevVel)

    index = 0
    prevProdNode = None
    prevTSNode = None
    startProdNode = Node.Node(state=startProdState, index=index,
                              obs=obs, adjList=[],
                              isAccepting=False, isVisited=False,
                              parent=prevProdNode)

    Nodes = []
    Nodes.append(startProdNode)
    index += 1

    nodeQueue = deque()
    nodeQueue.append((startProdNode, prevTSNode, startTSNode))
    accepts = []

    while nodeQueue:

        prevProdNode,\
            prevTSNode, currTSNode = nodeQueue.popleft()
        newProdNode = prevProdNode

        if not currTSNode.isVisited:

            currTSNode.isVisited = True
            keepSearching = True

            if (prevTSNode is not None) and (prevProdNode is not None):
                currObsv = currTSNode.obs

                currState = currTSNode.state

                carX = currState.carX
                carY = currState.carY
                carT = currState.carT
                prevLane = currState.prevLane
                prevVel = currState.prevVel

                qNew = LDBA.DFA.transFcn(prevProdNode.state.q, currObsv)
                qNewAccepts = (qNew in LDBA.DFA.accepts)

                newProdState = Node.NodeState(carX, carY, carT, qNew,
                                              prevLane, prevVel)
                newProdNode = Node.Node(state=newProdState, index=index,
                                        isAccepting=qNewAccepts,
                                        parent=prevProdNode)

                # anything Node after reaching state 1 will not work
                keepSearching = (qNew != 1)
                if keepSearching:
                    accepts.append(index)
                    prevProdNode.adjList.append(newProdNode)

                # turn on for debug :)
                # print('X:', carX,
                #       'Y:', carY,
                #       'T:', carT,
                #       'index:', newProdNode.index,
                #       'parentIdx:', newProdNode.parent.index,
                #       'prevLane:', prevLane,
                #       'q:', qNew,
                #       'atGoal:', currObsv.atGoal,
                #       'crashed:', currObsv.crashed,
                #       'speeding:', currObsv.speeding,
                #       'keepSearching:', keepSearching)

                # goal state is defined in LDBA as q = 2
                atGoal = (qNew == 2)
                if atGoal:
                    return newProdNode

                index += 1

            if keepSearching:
                # now need after we have relaxed some of da edges its time to
                # do the BFS queuing
                for neighbor in currTSNode.adjList:
                    if not neighbor.isVisited:
                        nodeQueue.append((newProdNode, currTSNode, neighbor))

    # if you get here things have gone horribly wrong
    return None


#
# @brief      Gets the path to root from leaf of the DFA
#
# @param      leaf  The leaf Node object
#
# @return     A list of Node objects with the root at index = 0 and the leaf at
#             the last index
#
def getPathToRootFromLeaf(leaf):

    currNode = leaf
    nodeQueue = deque()
    Nodes = []

    # putting nodes in a stack so we can reverse their order
    while currNode is not None:
        nodeQueue.append(currNode)
        currNode = currNode.parent

    # popping the stack into an array of Node, which containt the ordered path
    # from the root to the leaf Node.
    while nodeQueue:
        currNode = nodeQueue.pop()
        Nodes.append(currNode)

        state = currNode.state

        print('Lane:', state.carX,
              'Distance:', state.carY,
              'Time:', state.carT,
              'Velocity:', state.prevVel)

    return Nodes
