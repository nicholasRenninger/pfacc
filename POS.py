from __future__ import print_function
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


#
# @brief      Makes a Physical Occupancy Set Matrix. This matrix is basically a
#             binary, 3D matrix that indicates where is the road discretization
#             other vehicles (obstacles) exists
#
# The other cars' locations are drawn from uniform distributions and then
# transformed to distribute them properly
#
# @param      allLanes              A list of all possible lane numbers on the
#                                   highway.
# @param      allowedLaneVelocites  The allowed lane velocities tuple for a
#                                   certain lane number
# @param      maxDist               The maximum simulation distance
# @param      maxTime               The maximum simulation time
# @param      initCarX              The initial carX state. CarX ~ lane on
#                                   highway
# @param      initCarY              The initial carY state. CarY ~ distance
#                                   down highway
#
# @return     POS matrix given the simulation conditions
#
def makePOS(allLanes, allowedLaneVelocites, maxDist, maxTime,
            initCarX, initCarY):

    spaceFactor = 6

    numLanes = max(allLanes) + 1
    POS = np.zeros((numLanes, maxDist, maxTime))

    for ii in range(0, numLanes):

        # generating the spacing for the random other cars
        currLaneVelocityRange = allowedLaneVelocites[ii]
        minAllowedVelInLane = min(currLaneVelocityRange)
        dist = random.randint(0, minAllowedVelInLane * spaceFactor)

        # generating the obstacles for one time slice
        while dist < maxDist:
            POS[ii, dist, 0] = 1
            dist = dist + random.randint(0, minAllowedVelInLane * spaceFactor)

        # make sure to delete any other car that happens to be at the initial
        # state of our car
        POS[initCarX, initCarY, 0] = 0

        # propagating them forward through the time dimension of the occupancy
        # set
        for time in range(0, maxTime - 1):
            vbuf = (time + 1) * minAllowedVelInLane
            POS[ii, (vbuf + 1):, time + 1] = POS[ii, 1:-vbuf, 0]

    return POS


#
# @brief      Plots the POS matrix as well as the optimal path the car takes
#             through the road over successive time steps
#
# @param      POSMat       The POS matrix object
# @param      optimalPath  The optimal path, which is a list of Node objects
# @param      saveTitle  The save path string
# @param      initCarY     The initial downrange distance of the car
# @param      allLanes     All possible lane indices in a tuple
# @param      goalStates   The goal states - a list of (x, y)
# @param      maxTime      The maximum simulation time
#
# @return     a plot
#
def plotCarAndPOS(POSMat, optimalPath, saveTitle,
                  initCarY, allLanes, goalStates, maxTime):

    fig = plt.figure()
    image = plt.imread('car.png')
    shouldSavePlot = True

    # make a subplot for the state of the road for each time step
    for t in range(0, maxTime):

        ax = fig.add_subplot(3, 2, t + 1)

        # making the axis look like asphalt
        ax.set_facecolor((0.156, 0.149, 0.129))

        # Load images

        dat = POSMat[:, :, t]

        ########################################################
        # plotting the other cars on the road
        ########################################################

        nonZerosOrig = np.nonzero(dat)
        nonZerosFilt = []
        nonZerosFilt.append([])
        nonZerosFilt.append([])

        # car can't start at the very beginning of sim track, so trim off the
        # irrelevant beginning obstacle car states
        for ii in range(0, len(nonZerosOrig[0])):
            if nonZerosOrig[1][ii] >= initCarY:
                nonZerosFilt[0].append(nonZerosOrig[0][ii])
                nonZerosFilt[1].append(nonZerosOrig[1][ii])

        otherCarPos = np.array([nonZerosFilt[0], nonZerosFilt[1]])
        otherCarlanes = otherCarPos[0]

        # re-normalize all trimmed distances to be distances from the car's
        # starting location
        otherCarDistances = otherCarPos[1] - initCarY
        ax.plot(otherCarDistances, otherCarlanes, 'rs',
                markersize=11, label='Other Cars')

        ########################################################
        # plotting the lanes of the road
        ########################################################

        xCoordsOfOtherCars = np.array(range(len(otherCarDistances))) *\
            max(otherCarDistances) / len(otherCarDistances)

        for lanePos in range(min(allLanes) - 1, max(allLanes) + 2):
            lane = np.repeat(lanePos + 0.5, len(otherCarDistances))
            ax.plot(xCoordsOfOtherCars, lane, 'w--',
                    label=None)

        ########################################################
        # plotting the goal states
        ########################################################

        xGoal = []
        yGoal = []
        for state in goalStates:
            # re-normalize all trimmed distances to be distances from the car's
            # starting location
            xGoal.append(state[1] - initCarY)
            yGoal.append(state[0])

        minYGoal = min(yGoal) - 0.5
        maxYGoal = max(yGoal) + 0.5

        ax.fill_between(xGoal, minYGoal, maxYGoal,
                        alpha=0.5, color='green', label='Goal Region')

        ########################################################
        # plotting the car's position at time t
        ########################################################

        currCarState = optimalPath[t].state

        # re-normalize all trimmed distances to be distances from the car's
        # starting location
        carY = currCarState.carY - initCarY
        carX = currCarState.carX

        imscatter(carY, carX, image, zoom=0.04, ax=ax)

        ########################################################
        # plot labeling
        ########################################################

        # never describe your figures
        # ax.legend(fancybox=True, framealpha=0.5, loc='upper right')
        ax.set_title('Time Step = %d' % t)
        ax.set_xlabel('Distance')

        ########################################################
        # plot formatting
        ########################################################

        minY = min(allLanes) - 0.6
        maxY = max(allLanes) + 0.6
        maxX = min(xGoal) * 1.2
        minX = 0

        plt.xlim((minX, maxX))
        plt.ylim((minY, maxY))
        ax.axes.get_yaxis().set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.8)
    if shouldSavePlot:
        fig = plt.gcf()
        fig.canvas.manager.full_screen_toggle()
        fig.show()
        fig.set_size_inches((11, 8.5), forward=False)
        plt.savefig(saveTitle, dpi=500)
        print('wrote figure to ', saveTitle)
    plt.show()


#
# @brief      This is black magic
#
# @param      x      x plot location
# @param      y      y plot location
# @param      image  The image path
# @param      ax     the axes artist object
# @param      zoom   The zoom level for the image
#
# @return     list of artist objects for all of da (x,y) pairs
#
def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists
