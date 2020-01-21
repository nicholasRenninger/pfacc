import Node
import PDFA


class S_PDFA:

    #
    # @brief      class representing the specification beta Accepting
    #             Probabilisitic Deterministic Finite Automata (S_PDFA)
    #
    def __init__(self):

        state0 = Node.NodeState(q=0)
        state1 = Node.NodeState(q=1)
        state2 = Node.NodeState(q=2)

        node0 = Node.Node(state=state0, index=0, isAccepting=False)
        node1 = Node.Node(state=state1, index=1, isAccepting=False)
        node2 = Node.Node(state=state2, index=2, isAccepting=True)

        accepts = [2]

        startNode = node0

        Nodes = []
        Nodes.append(node0)
        Nodes.append(node1)
        Nodes.append(node2)

        def transFcn(q, obs):

            if q == 0:
                if obs.atGoal and (not obs.crashed) and (not obs.speeding):
                    return 2
                elif obs.crashed or obs.speeding:
                    return 1
                else:
                    return 0

            elif q == 1:
                return 1

            elif q == 2:
                if obs.crashed or obs.speeding:
                    return 1
                else:
                    return 2

        self.DFA = PDFA.PDFA(nodes=Nodes, startNode=startNode,
                             transFcn=transFcn, accepts=accepts)
