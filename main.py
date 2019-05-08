from graph import Graph
from OS_Calls import clear_screen
from plotting import plot_n_vs_k

from numpy import random
import matplotlib.pyplot as plt


def main():

    clear_screen()

    # plot settings
    plt.close('all')
    figureFolder = '../Figures/'
    saveType = '.pdf'
    legendStr = ['Basic BFS', 'Bi-Directional BFS']

    debug = False

    # testing functionality of BFS functions
    print('=====================================')
    print('------------ BFS TESTING ------------')
    print('=====================================')
    verts = [1, 2, 3, 4, 5, 6, 7, 8,
             9, 10, 11, 12, 13, 14]
    labels = ['V1', 'V2', 'V3', 'V4', 'V5',
              'V6', 'V7', 'V8', 'V9', 'V10',
              'V11', 'V12', 'V13', 'V14']
    edges = [(1, 2), (1, 7),
             (2, 1), (2, 3), (2, 7), (2, 8),
             (3, 2), (3, 4), (3, 8),
             (4, 3), (4, 5), (4, 9), (4, 10),
             (5, 4), (5, 6), (5, 10), (5, 11),
             (6, 5), (6, 11),
             (7, 1), (7, 2), (7, 8),
             (8, 2), (8, 3), (8, 7), (8, 9),
             (9, 4), (9, 8), (9, 10), (9, 12),
             (10, 4), (10, 5), (10, 9), (10, 11), (10, 13),
             (11, 5), (11, 6), (11, 10), (11, 13), (11, 14),
             (12, 9), (12, 13),
             (13, 10), (13, 11), (13, 12), (13, 14),
             (14, 11), (14, 13)]

    # unweighted, for now...
    edgeWeight = 1
    edgeWeights = [edgeWeight for i in range(0, len(edges))]

    randEdges = random.permutation(edges)
    randVertsIDX = random.permutation(range(0, len(verts)))
    randVerts = [verts[i] for i in randVertsIDX]
    randLabels = [labels[i] for i in randVertsIDX]

    graph_test = Graph(randVerts, randLabels, randEdges, edgeWeights)
    # graph_test = Graph(verts, labels, edges, edgeWeights)

    graph_test.dispEdges()
    graph_test.test_BFSvsBiBFS()

    # Grid graphs
    print('\n=====================================')
    print('------------ GRID GRAPHS ------------')
    print('=====================================')

    # plotting
    n_list = range(3, 20 + 1)
    k_lists = ([], [])

    for N in n_list:
        print('\n###################################')
        print('N =', N)
        gridGraph = Graph()
        gridGraph.buildNGrid(N)
        # gridGraph.dispEdges()

        # find path from right and left edges of grid.
        # break ties if N is even by rounding up, towards zero with int()
        src = int(N / 2) * N + 1
        dst = src + N - 1
        source = 'V' + str(src)
        dest = 'V' + str(dst)
        print('Source: ', source, '    Dest: ', dest, sep='')

        # build up lists of distances and dequeues for comparison
        d1, k1 = gridGraph.BFS(source, dest)
        d2, k2 = gridGraph.biDirectionalBFS(source, dest, debug)

        k_lists[0].append(k1)
        k_lists[1].append(k2)

        print('____________________________________')
        print('Algorithm', '   Dist', '     ', 'Num. Dequeues')
        print('____________________________________')
        print('   BFS      ', d1, '         ', k1)
        print('bi-BFS      ', d2, '         ', k2)
        print('____________________________________')

    # make the plot
    saveTitle = figureFolder + 'BFS_vs_BiBFS_grid' + saveType
    plotTitle = 'BFS vs. Bi-Directional BFS for Grid Graph'
    ylabel = 'Number of Dequeue Operations, $k_n$'
    xlabel = 'Size of Graph, $n$: $|V| = n^2$, $|E| = 2n^2-2n$'
    plot_n_vs_k((n_list, n_list), k_lists, plotTitle, saveTitle, xlabel,
                ylabel, legendStr)

    # Trees graphs
    print('\n=====================================')
    print('------------ TREE GRAPHS ------------')
    print('=====================================')

    # plotting
    n_list = range(3, 15 + 1)
    k_lists = ([], [])

    for N in n_list:

        print('\n###################################')
        print('N =', N)
        treeGraph = Graph()
        treeGraph.buildNTree(N)

        # find path from root to leaf node at depth N.
        # pick and node at that depth
        src = 1
        dst = 2 ** (N) - 1
        source = 'V' + str(src)
        dest = 'V' + str(dst)
        print('Source: ', source, '    Dest: ', dest, sep='')

        # build up lists of distances and dequeues for comparison
        d1, k1 = treeGraph.BFS(source, dest)
        d2, k2 = treeGraph.biDirectionalBFS(source, dest, debug)

        k_lists[0].append(k1)
        k_lists[1].append(k2)

        print('____________________________________')
        print('Algorithm', '   Dist', '     ', 'Num. Dequeues')
        print('____________________________________')
        print('   BFS      ', d1, '         ', k1)
        print('bi-BFS      ', d2, '         ', k2)
        print('____________________________________')

    # make the plot
    plotTitle = 'BFS vs. Bi-Directional BFS for Complete Binary Tree'
    saveTitle = figureFolder + 'BFS_vs_BiBFS_tree' + saveType
    ylabel = 'Number of Dequeue Operations, $k_n$'
    xlabel = 'Size of Graph, $n$: $|V| = n$, $|E| = 2^n - 1$'
    plot_n_vs_k((n_list, n_list), k_lists, plotTitle, saveTitle, xlabel,
                ylabel, legendStr)

    # random graphs
    print('\n=====================================')
    print('------------ RAND GRAPHS ------------')
    print('=====================================')

    numTrials = 50

    # plotting
    n_list = range(3, 20 + 1)
    k_lists = ([], [])

    # size of each graph
    for N in n_list:

        print('\n###################################')
        print('N =', N)

        # find path from root to leaf node at depth N.
        # pick and node at that depth
        src = 1
        dst = 2
        source = 'V' + str(src)
        dest = 'V' + str(dst)
        print('Source: ', source, '    Dest: ', dest, sep='')

        avgd1 = 0
        avgk1 = 0
        avgd2 = 0
        avgk2 = 0

        i = 0
        totTrials = 0

        # run the trial numTrials times
        while i <= numTrials:

            randGraph = Graph()
            randGraph.buildNRandGraph(N)

            # build up lists of distances and dequeues for comparison
            d1, k1 = randGraph.BFS(source, dest)
            d2, k2 = randGraph.biDirectionalBFS(source, dest, debug)

            # re-make the graph and try again if no path was found in random
            # graph
            if d1 is None or d2 is None or k1 is None or k2 is None:
                d1 = 0
                d2 = 0
                k1 = 0
                k2 = 0
                i -= 1

            avgd1 += d1
            avgk1 += k1
            avgd2 += d2
            avgk2 += k2

            i += 1
            totTrials += 1

        # average results
        d1_avg = avgd1 / numTrials
        k1_avg = avgk1 / numTrials
        d2_avg = avgd2 / numTrials
        k2_avg = avgk2 / numTrials

        k_lists[0].append(k1_avg)
        k_lists[1].append(k2_avg)

        print('Number of Desired Trials:', numTrials)
        print('Actual Number of Non-Null Trials Needed:', totTrials)
        print('____________________________________')
        print('Algorithm', '   Dist', '     ', 'Num. Dequeues')
        print('____________________________________')
        print('   BFS      ', d1_avg, '         ', k1_avg)
        print('bi-BFS      ', d2_avg, '         ', k2_avg)
        print('____________________________________')

    # make the plot
    plotTitle = 'BFS vs. Bi-Directional BFS for Randomly Generated Graph'
    saveTitle = figureFolder + 'BFS_vs_BiBFS_rand' + saveType
    ylabel = 'Avg. Number of Dequeue Operations, $k_n$'
    xlabel = 'Size of Graph, $n$: $|V| = n$, $|E| = O(n^2)$'
    plot_n_vs_k((n_list, n_list), k_lists, plotTitle, saveTitle, xlabel,
                ylabel, legendStr)

    # show all figures at the end
    plt.show()


main()
