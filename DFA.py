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

    startTSNode = TS.DFA.startNode
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
    startProdNode = Node.Node(state=startProdState, index=index,
                              obs=obs, isAccepting=False, isVisited=False)
    Nodes = []
    Nodes.append(startProdNode)
    index += 1

    nodeQueue = deque()
    nodeQueue.append((None, startProdNode))
    accepts = []

    while nodeQueue:

        prevNode, currNode = nodeQueue.popleft()

        if not currNode.isVisited:

            currNode.isVisited = True
            if prevNode is not None:
                currObsv = currNode.obs

                currState = currNode.state

                carX = currState.carX
                carY = currState.carY
                carT = currState.carT
                prevLane = currState.prevLane
                prevVel = currState.prevVel

                qNew = LDBA.DFA.transFcn(prevNode.state.q, currObsv)
                qNewAccepts = (qNew in LDBA.DFA.accepts)

                newProdState = Node.NodeState(carX, carY, carT, qNew,
                                              prevLane, prevVel)
                newProdNode = Node.Node(state=newProdState, index=index,
                                        isAccepting=qNewAccepts,
                                        parent=prevNode)

                # anything after state 1 will not work
                keepSearching = (qNew != 1)
                if keepSearching:
                    accepts.append(index)
                    prevNode.adjList.append(newProdNode)

                # goal state is defined in LDBA as q = 2
                atGoal = (qNew == 2)
                if atGoal:
                    return newProdNode

                index += 1

                print(carX, carY, carT, prevLane, qNew, currObsv)

            if keepSearching:
                # now need after we have relaxed some of da edges its time to
                # do the BFS queuing
                for neighbor in currNode.adjList:
                    if not neighbor.isVisited:
                        nodeQueue.append((currNode, neighbor))

    # if you get here things have gone horribly wrong
    return None
