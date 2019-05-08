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
# @param      TS    A TransistionSystem to product with the LBDA, containing
#                   the physical modeling transitions
# @param      LDBA  The LDBA (LTL Deterministic Buchi Automata) encoding the
#                   LTL specification on TS
#
# @return     the first Node object in the product to accept
#
def formAndSolveProduct(TS, LDBA):

    startTSNode = TS.startNode
    startLDBANode = LDBA.startNode

    startTSState = startTSNode.state
    carX = startTSState.carX
    carY = startTSState.carY
    carT = startTSState.carT
    prevLane = startTSState.prevLane
    prevVel = startTSState.prevVel

    q = startLDBANode.state.q

    startProdState = Node.NodeState(carX, carY, carT, q, prevLane, prevVel)

    index = 0
    startProdNode = Node.Node(state=startProdState, index=index,
                              isAccepting=False, isVisited=False)
    Nodes = []
    Nodes.append(startProdNode)
    index += 1

    nodeQueue = deque()
    nodeQueue.append((None, startProdNode))
    accepts = []

    while nodeQueue:

        prevNode, currNode = nodeQueue.popleft()
        currTSNode = currNode[0]

        if not currTSNode.isVisited:

            currTSNode.isVisited = True
            if prevNode is not None:
                currObsv = currTSNode.obs

                prevLDBANode = prevNode[1]
                newLDBANode = LDBA.transFcn(prevLDBANode.index, currObsv)

                currTSState = currTSNode.state

                carX = currTSState.carX
                carY = currTSState.carY
                carT = currTSState.carT
                prevLane = currTSState.prevLane
                prevVel = currTSState.prevVel

                q = newLDBANode.state.q

                newProdState = Node.NodeState(carX, carY, carT, q,
                                              prevLane, prevVel)
                newProdNode = Node.Node(state=newProdState, index=index,
                                        isAccepting=newLDBANode.isAccepting,
                                        parent=prevNode)

                if newProdNode.isAccepting:
                    accepts.append(index)
                    prevNode.adjList.append(newProdNode)

                # goal state is defined in LDBA as q = 2
                atGoal = (q == 2)
                if atGoal:
                    return newProdNode

                index += 1

                # now need after we have relaxed some of da edges its time to
                # do the BFS queuing
                for neighbor in currTSNode.adjList:
                    if not neighbor.isVisited:
                        nodeQueue.append((currNode, neighbor))

    # if you get here things have gone horribly wrong
    return None
