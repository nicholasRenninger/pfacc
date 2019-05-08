from collections import deque
from random import random


class Vertex:

    def __init__(self, label, num):
        """
        Graph.__init__(self, label, num)
        creates an instance of a potentially weighted, directed vertex in graph

        :param label: string or int name for the vertex, not its index
        :type label: (int) or (str)
        :param num: vertex index
        :type num: int

        :returns: initialized graph vertex
        :rtype: custom vertex object
        """

        self.label = label
        self.num = num
        self.adj = []
        self.WeightTo = {}

        # 2 states for bidirectional BFS
        # each state either: 'unvisited' or 'visited'
        self.layerSrc = None
        self.layerDest = None
        self.predSrc = None
        self.predDest = None
        self.distSrc = None
        self.distDest = None
        self.visitedMarker = 1
        self.unvisitedMarker = 0
        self.stateSrc = self.unvisitedMarker
        self.stateDest = self.unvisitedMarker


class Graph:

    def __init__(self, vertices=[], vertLabels=[], edges=[], edgeWeights=[]):
        """
        Graph.__init__(self, vertices, vertLabels, edges, edgeWeights)
        creates and stores the given list of vertices and edges as an
        adjancency list.

        :param vertices: list of vertices making up the graph
        :type vertices: list of (int)
        :param vertices: list of vertices making up the graph
        :type vertLabels: list of labels for each vertex. can be string or int
        :param vertLabels: list of (int) or (str).
        len(vertLabels) = len(vertices)
        :type edges: list(tuples(int))
        :param edgeWeights: list of ints containing the weight of each edge.
        same size as edges.
        :type edges: list(int)

        :returns: initialized graph object stored as an adjancency list
        :rtype: custom graph object
        """
        self.verts = {}
        self.labels = {}
        self.vertKeys = {}
        self.buildGraph(vertices, vertLabels, edges, edgeWeights)

    def buildGraph(self, vertices, vertLabels, edges, edgeWeights):
        """
        Graph.buildGraph(self, vertices, vertLabels, edges, edgeWeights)
        creates and stores the given list of vertices and edges as an
        adjancency list.

        :param vertices: list of vertices making up the graph
        :type vertices: list of (int)
        :param vertices: list of vertices making up the graph
        :type vertLabels: list of labels for each vertex. can be string or int
        :param vertLabels: list of (int) or (str).
        len(vertLabels) = len(vertices)
        :type edges: list(tuples(int))
        :param edgeWeights: list of ints containing the weight of each edge.
        same size as edges.
        :type edges: list(int)

        :returns: initialized graph object stored as an adjancency list
        :rtype: custom graph object
        """

        for i in range(0, len(vertices)):
            self.addVert(vertLabels[i], vertices[i])

        for j in range(0, len(edges)):
            source = self.verts[edges[j][0]]
            dest = self.verts[edges[j][1]]

            self.addEdge(source, dest, edgeWeights[j])

        return self

    def buildNGrid(self, N):
        """
        self.buildNGrid(self, N)
        creates and stores the given list of vertices and edges as an
        adjancency list. Nodes are numbered starting at 1 (left, top corner),
        increasing across rows, and with the bottom right node's num = N^2.
        Graph is undirected, unweighted, simple. N > 3
        ex: N = 3
            1 - 2 - 3
            |   |   |
            4 - 5 - 6
            |   |   |
            7 - 8 - 9

        :param N: N value, where graph is a NxN grid of vertices arranged NSEW
        :type N: int
        """

        # unweighted graph
        edgeWt = 1

        numVert = N ** 2

        for i in range(1, numVert + 1):
            self.addVert('V' + str(i), i)

        # define corners
        LT = 1
        RT = N
        LB = N * (N - 1) + 1
        RB = N ** 2

        # define range node numbers for top/bottom row, and left/right cols
        T_row = [i for i in range(2, RT, 1)]
        L_col = [i for i in range(1 + N, LB, N)]
        B_row = [i for i in range(LB + 1, RB, 1)]
        R_col = [i for i in range(N + N, N ** 2, N)]

        # add edges based on position in graph
        for i in range(1, numVert + 1):

            src = self.verts[i]

            # top left corner
            if i == LT:
                dst = self.verts[i + N]
                dst1 = self.verts[i + 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)

            # top right corner
            elif i == RT:
                dst = self.verts[i + N]
                dst1 = self.verts[i - 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)

            # bottom left corner
            elif i == LB:
                dst = self.verts[i - N]
                dst1 = self.verts[i + 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)

            # bottom right corner
            elif i == RB:
                dst = self.verts[i - N]
                dst1 = self.verts[i - 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)

            # top row
            elif i in T_row:
                dst = self.verts[i - 1]
                dst1 = self.verts[i + 1]
                dst2 = self.verts[i + N]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)
                self.addEdge(src, dst2, edgeWt)

            # bottom row
            elif i in B_row:
                dst = self.verts[i - 1]
                dst1 = self.verts[i + 1]
                dst2 = self.verts[i - N]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)
                self.addEdge(src, dst2, edgeWt)

            # left col
            elif i in L_col:
                dst = self.verts[i - N]
                dst1 = self.verts[i + N]
                dst2 = self.verts[i + 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)
                self.addEdge(src, dst2, edgeWt)

            # right col
            elif i in R_col:
                dst = self.verts[i - N]
                dst1 = self.verts[i + N]
                dst2 = self.verts[i - 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)
                self.addEdge(src, dst2, edgeWt)

            # middle
            else:
                dst = self.verts[i + N]
                dst1 = self.verts[i - N]
                dst2 = self.verts[i + 1]
                dst3 = self.verts[i - 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)
                self.addEdge(src, dst2, edgeWt)
                self.addEdge(src, dst3, edgeWt)

    def buildNTree(self, N):
        """
        self.buildNTree(self, N)
        creates and stores the given list of vertices and edges as an
        adjancency list. Nodes are numbered starting at 1 (root of tree),
        increasing across each level of the tree, and with the bottom right
        leaf's number being = 2^N - 1.
        Graph is an undirected balanced binary tree. N > 3
        ex: N = 3
                1
              /   \
             2     3
           /   \  /  \
          4    5  6   7

        :param N: N value, where graph is a balanced binary tree of depth N
        :type N: int
        """

        # unweighted graph
        edgeWt = 1

        numVert = 2 ** N - 1

        for i in range(1, numVert + 1):
            self.addVert('V' + str(i), i)

        for i in range(1, numVert + 1):

            src = self.verts[i]

            # root
            if i == 1:
                dst = self.verts[i + 1]
                dst1 = self.verts[i + 2]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)

            # all internal nodes
            elif i <= 2 ** (N - 1) - 1:
                dst = self.verts[int(i / 2)]
                dst1 = self.verts[2 * i]
                dst2 = self.verts[2 * i + 1]

                self.addEdge(src, dst, edgeWt)
                self.addEdge(src, dst1, edgeWt)
                self.addEdge(src, dst2, edgeWt)

            # all leaf nodes
            else:
                dst = self.verts[int(i / 2)]

                self.addEdge(src, dst, edgeWt)

    def buildNRandGraph(self, N):
        """
        self.buildNRandGraph(self, N)
        creates and stores the given list of vertices and edges as an
        adjancency list. Nodes are numbered from 1 to N. There is a 50% chance
        that an edge is added between each node => up to N^2 nodes
        N > 3
        :param N: N value, where graph has |V| = N and O(N^2) randomly chosen
                  vertices
        :type N: int
        """

        # unweighted graph
        edgeWt = 1

        numVert = N

        for i in range(1, numVert + 1):
            self.addVert('V' + str(i), i)

        # randomly choose if edge (x, y) is created
        for x in range(1, numVert + 1):
            for y in range(1, numVert + 1):

                src = self.verts[x]
                dst = self.verts[y]

                # randomly choose whether edge is taken
                if random() > 0.5:
                    self.addEdge(src, dst, edgeWt)

    def addVert(self, label, num):
        """
        Graph.addVert(self, label, num)
        add a given vertex with label and index num to the dictionary
        of vertices in graph

        :param label: string or int name for the vertex, not its index
        :type label: (int) or (str)
        :param num: vertex index
        :type num: int

        :returns: nothing
        :rtype: N/A
        """
        newVert = Vertex(label, num)
        self.verts[num] = newVert
        self.labels[num] = label
        self.vertKeys[label] = num

    def addEdge(self, source, dest, edgeWeight):
        """
        addEdge(self, source, dest, edgeWeight)
        adds an edge between the source and destination vertices, with
        the given edge weight

        :param source: beginning vertex of the graph
        :type source: vertex object
        :param dest: end vertex of the graph
        :type dest: vertex object
        :param edgeweight: weight of the edge to be added
        :type num: int

        :returns: nothing
        :rtype: N/A
        """
        source.adj.append(dest)
        source.WeightTo[dest] = edgeWeight

    def dispEdges(self):
        """
        dispEdges(self)
        prints the adjancency list using the defined vertex labels

        :returns: nothing
        :rtype: N/A
        """

        if len(self.verts) == 0:
            print('Empty Graph')
            return

        print('Source Vertex: Connected Destination Vertices', end='')
        for vNum, vertex in self.verts.items():
            print('\n', vertex.label, ': ', sep='', end='')
            hasSeen = False
            if len(vertex.adj) == 0:
                print('None', end='')
            for edge in vertex.adj:
                if hasSeen:
                    print(', ', edge.label, sep='', end='')
                else:
                    print(edge.label, sep='', end='')
                    hasSeen = True
        print('\n')

    def BFS(self, sourceLabel, destLabel):
        """
        BFS(self, sourceLabel, destLabel)
        does BFS on the graph to calculate, in the case that graph is
        unweighted, undirected, simple graphs, the shortest path from
        source to dest.

        :param sourceLabel: label of the starting vertex to consider
        :type sourceLabel: (str)
        :param destLabel: label of the ending vertex to consider
        :type destLabel: (str)

        :returns: the distance from source -> dest in the unweighted,
                  undirected, simple graph and the number of dequeues done
                  during the course of the entire algorithm.
                  (dist, numDequeues)
        :rtype: tuple(int, int)
        """

        # make sure the chosen vertices is actually in the graph
        try:
            source = self.verts[self.vertKeys[sourceLabel]]
            dest = self.verts[self.vertKeys[destLabel]]
        except Exception as e:
            print("chosen start and/or end vert not valid: ", str(e))
            return (None, None)

        # set the state of all vertices to be in their default state
        self.reset()

        numDequeues = 0

        # queue needs to hold tuples of:
        # (parentVertex, currentVertex)
        vertexFrontierQueue = deque()
        vertexFrontierQueue.append((None, source))

        # if the queue is not empty, there are still unvisited nodes
        while vertexFrontierQueue:

            # for BFS, use FIFO queue -> popleft()
            prevVert, currVert = vertexFrontierQueue.popleft()
            numDequeues += 1

            if currVert.stateSrc == currVert.unvisitedMarker:

                # mark currVert as visited, parent node, and the distance from
                # soruce to currVert
                currVert.stateSrc = currVert.visitedMarker
                currVert.predSrc = prevVert

                if prevVert is not None:
                    currVert.distSrc = (prevVert.distSrc +
                                        prevVert.WeightTo[currVert])
                else:
                    currVert.distSrc = 0

                # break BFS early, when it finds dest, instead of searching
                # whole graph
                if currVert == dest:
                    return (currVert.distSrc, numDequeues)

                for neighbor in currVert.adj:
                    if neighbor.stateSrc == neighbor.unvisitedMarker:
                        vertexFrontierQueue.append((currVert, neighbor))

        # if the queue is empty and we haven't returned, there is no path from
        # source to dest
        # print('No path found from source', source.label, '->', dest.label)
        return (None, 0)

    def biDirectionalBFS(self, sourceLabel, destLabel, debug):
        """
        biDirectionalBFS(self, sourceLabel, destLabel)
        does bi-directional BFS on the graph to calculate, in the case that
        graph is unweighted, undirected, simple graphs, the shortest path from
        source to dest.

        :param sourceLabel: label of the starting vertex to consider
        :type sourceLabel: (str)
        :param destLabel: label of the ending vertex to consider
        :type destLabel: (str)
        :param debug: turns on or off extra printing
        :type debug: bool

        :returns: the distance from source -> dest in the unweighted,
                  undirected, simple graph and the number of dequeues done
                  during the course of the entire algorithm.
                  (distSrc, numDequeues)
        :rtype: tuple(int, int)
        """

        # make sure the chosen vertices is actually in the graph
        try:
            source = self.verts[self.vertKeys[sourceLabel]]
            dest = self.verts[self.vertKeys[destLabel]]
        except Exception as e:
            print("chosen start and/or end vert not valid: ", str(e))
            return (None, None)

        # set the state of all vertices to be in their default state
        self.reset()

        numDequeues = 0

        # queue needs to hold tuples of:
        # (parentVertex, currentVertex)
        vertexSourceQueue = deque()
        vertexDestQueue = deque()
        vertexSourceQueue.append(source)
        vertexDestQueue.append(dest)

        source.distSrc = 0
        dest.distDest = 0

        # if the queue is not empty, there are still unvisited nodes
        while vertexSourceQueue and vertexDestQueue:

            # working from source vertex forward
            if vertexSourceQueue:

                # for BFS, use FIFO queue -> popleft()
                currVert = vertexSourceQueue.popleft()
                numDequeues += 1
                prevVert = currVert.predSrc

                if currVert.stateSrc == currVert.unvisitedMarker:
                    # mark currVert as visited, parent node, and the distance
                    # from source to currVert
                    currVert.stateSrc = currVert.visitedMarker
                    if prevVert is not None:
                        currVert.distSrc = (prevVert.distSrc +
                                            prevVert.WeightTo[currVert])

                    if prevVert is not None:
                        currVert.distSrc = (prevVert.distSrc +
                                            prevVert.WeightTo[currVert])
                    else:
                        currVert.distSrc = 0

                    # break BFS early, when it finds dest, instead of searching
                    # whole graph
                    if currVert == dest:
                        return (currVert.distSrc, numDequeues)

                    for neighbor in currVert.adj:

                        if neighbor.predSrc is None:
                            neighbor.predSrc = currVert
                        if neighbor.stateSrc == neighbor.unvisitedMarker:
                            vertexSourceQueue.append(neighbor)

                if currVert == dest or currVert in vertexDestQueue:
                    if currVert.predDest is not None:
                        if currVert.predSrc is not None:
                            dist = (currVert.distSrc +
                                    currVert.predDest.distDest +
                                    currVert.predDest.WeightTo[currVert])
                        else:
                            dist = currVert.distSrc

                    return (dist, numDequeues)

            # working from dest vertex forward
            if vertexDestQueue:

                # for BFS, use FIFO queue -> popleft()
                currVert = vertexDestQueue.popleft()
                numDequeues += 1
                prevVert = currVert.predDest

                if currVert.stateDest == currVert.unvisitedMarker:
                    # mark currVert as visited, parent node, and the distance
                    # from dest to currVert
                    currVert.stateDest = currVert.visitedMarker

                    if prevVert is not None:
                        currVert.distDest = (prevVert.distDest +
                                             prevVert.WeightTo[currVert])

                    # break BFS early, when it finds source, instead of
                    # searching whole graph
                    if currVert == source:
                        return (currVert.distDest, numDequeues)

                    for neighbor in currVert.adj:
                        if neighbor.predDest is None:
                            neighbor.predDest = currVert
                        if neighbor.stateDest == neighbor.unvisitedMarker:
                            vertexDestQueue.append(neighbor)

                if currVert == source or currVert in vertexSourceQueue:
                    if currVert.predSrc is not None:
                        dist = (currVert.distDest +
                                currVert.predSrc.distSrc +
                                currVert.predSrc.WeightTo[currVert])
                    else:
                        dist = currVert.distDest
                    return (dist, numDequeues)

        # if the queue is empty and we haven't returned, there is no path from
        # source to dest
        # print('No path found from source', source.label, '->', dest.label)
        return (None, None)

    def test_BFSvsBiBFS(self):
        """
        test_BFSvsBiBFS(self)
        Compares BFS with bi-directional BFS for each vertex pair in self

        :returns: whether BFS and bi-directional BFS returned same output for
                  every vertex pair in the self graph.
        :rtype: bool
        """
        passed = True
        debug = True

        for source in self.labels.values():
            for dest in self.labels.values():

                # print('\n#####################')
                # print(source, dest)
                (d1, k1) = self.BFS(source, dest)
                (d2, k2) = self.biDirectionalBFS(source, dest, debug)
                # print('d1:', d1, 'd2:', d2)
                # print('k1:', k1, 'k2:', k2)

                if d1 != d2:
                    passed = False
                    print('\n#####################')
                    print('Failed on ', source, ' -> ', dest, sep='')
                    if d1 is not None:
                        print('BFS Distance:', d1)
                        print('Number of dequeues needed:', k1)
                    if d2 is not None:
                        print('\nBi-Directional BFS Distance:', d2)
                        print('Number of dequeues needed:', k2)
        if passed:
            print('Test passed')
        else:
            print('Test failed')
        return passed

    def reset(self):
        """
        reset(self)
        resets all vertex indicator values
        """
        for vert in self.verts.values():

            # mark each vertex as unvisited
            vert.stateSrc = vert.unvisitedMarker
            vert.stateDest = vert.unvisitedMarker

            # mark them all as having no layer
            vert.layerSrc = None
            vert.layerDest = None

            # initialize predecessor array
            vert.predSrc = None
            vert.predDest = None

            # distance from source to vert
            vert.distSrc = None

            # distance from dest to vert
            vert.distDest = None

    def countPaths(self, sourceLabel, destLabel):
        """
        countPaths(self, sourceLabel, destLabel)
        counts the total number of paths in the graph, assuming the
        graph is a DAG, from the vertex labeled with the label in
        sourceLabel, and ending at the vertex labeled with the label
        destLabel

        :param sourceLabel: label of the starting vertex to consider
        :type sourceLabel: (str)
        :param destLabel: label of the ending vertex to consider
        :type destLabel: (str)

        :returns: number of paths between the source and dest vertices
        :rtype: int
        """

        # make sure the chosen vertices is actually in the graph
        try:
            source = self.vertices[sourceLabel]
            dest = self.verts[destLabel]
        except Exception as e:
            print("chosen start and/or end vert not valid: ", str(e))
            return None

        if source == dest:
            return 1
        else:
            if not source.distSrc:

                tempDist = 0

                for neighbor in source.adj:
                    tempDist += self.countPaths(neighbor.num, dest.num)

                source.distSrc = tempDist

            return source.distSrc

    def multiGraphReduce(self):
        """
        multiGraphReduce(self)
        efficiently convert the self.graph from a multigraph into a
        simple, directed graph with the same MST

        :returns: modifies self.verts and self.labels to get rid of redundant
        vertices in the original multigraph
        :rtype: None
        """

        # TODO:
        # this still seems to break the connectivity somehow...
        # BFS doesn't work after applying this to self

        for key in self.verts:

            currVert = self.verts[key]

            # need to create a temporary hashtable for each vertex that stores
            # which edges have already been seen, as well as create a new
            # vertex which will only have the reduced set of edges in it
            temp = {}
            newVert = Vertex(currVert.label, currVert.num)

            for currEdge in currVert.adj:

                # add this edge to the new, reduced graph it is not already in
                # the temporary hashtable
                currDest = currEdge.num
                if (currDest not in temp) and (currDest != currVert.num):

                    temp[currDest] = 1
                    newVert.adj.append(currEdge)

            # after we have built up the new vertex without the redundant edges
            # and loops, replace the old vertex with the new one
            self.verts[key] = newVert
