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
    return 1
