"""
This is the grid where the cluster grows.
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import os
from matplotlib import colors
from RandomWalker import Walker

class DLAgrid:
    def __init__(self, radius):
        self.radius = radius
        self.size = int(radius) * 2 + 5 # One cell for the central seed, two for the forbidden region.
        self.grid = np.zeros([self.size, self.size], int)
        for i in range(0, self.size): # Forbidden region marked as 2.
            for j in range(0, self.size):
                if i == radius + 2 and j == radius + 2:
                    self.grid[i][j] = 1
                elif self.distance(i, j, radius + 2, radius + 2) > radius:
                    self.grid[i][j] = 2
        self.boundary = self.findBoundary()
        self.releaseRegion = self.findReleaseRegion()
        # Code below will label the boundary and region releasing particles in different colors.
        '''for one in self.boundary:
            self.grid[one[0]][one[1]] = 3
        for one in self.releaseRegion:
            self.grid[one[0]][one[1]] = 4'''

    def distance(self, i, j, x, y):
        return np.sqrt((i - x) **2 + (j - y) **2)

    # Find the value of adjacent neighbors around one site.
    def findNeighbors(self, x, y):
        size = self.size
        neighbors = [self.grid[(x + 1) % size][y], self.grid[(x - 1) % size][y],
                    self.grid[x][(y + 1) % size], self.grid[x][(y - 1) % size]]
        return neighbors

    # Points at the boundary
    # One point is the boundary point if and only if both forbidden
    # point(=2) and vacant point(=0) are its neighbors.
    def findBoundary(self):
        size = self.size
        boundary = []
        for i in range(0, size):
            for j in range(0, size):
                if self.grid[i][j] == 0:
                    neighbors = self.findNeighbors(i, j)
                    if 0 in neighbors and 2 in neighbors:
                        boundary.append([i, j])
                    else:
                        pass
                else:
                    pass
        return boundary

    # Particles are not released right at the boundary, but at the place which
    # is away from the boundary by one site, so that the released particle will
    # not enter the forbidden region at the very start.
    def findReleaseRegion(self):
        region = []
        neighbors_of_Boundary = []
        for point in self.boundary:
            x, y = point[0], point[1]
            neighbors_of_Boundary.append([x + 1, y])
            neighbors_of_Boundary.append([x - 1, y])
            neighbors_of_Boundary.append([x, y + 1])
            neighbors_of_Boundary.append([x, y - 1])
        for point in neighbors_of_Boundary:
            x, y = point[0], point[1]
            if self.grid[x][y] == 0:
                neighbors = self.findNeighbors(x, y)
                if neighbors == [0, 0, 0, 0]:
                    region.append([x, y])
                else:
                    pass
            else:
                pass
        return region

    # Released particle randomly chooses a start point among those released sites.
    # Transforming a random angle in the polar coordinates is not recommended, for
    # that will lead to unequal probability to decide a start site.
    def aggregate(self):
        endFlag = True
        walkerCount = 0
        clusterCount = 0
        while endFlag:
            random.seed()
            startPoint = random.choice(self.releaseRegion)
            particle = Walker(startPoint[0], startPoint[1])
            walkerCount += 1
            while 1:
                neighbors = self.findNeighbors(particle.X, particle.Y)
                command = particle.checkAround(self.grid[particle.X][particle.Y], neighbors)
                if command == "continue":
                    particle.walk()
                else:
                    if command == "aggregated":
                        self.grid[particle.X][particle.Y] = 1
                        clusterCount += 1
                        break
                    elif command == "out":
                        break
                    else:
                        endFlag = False
                        break
            if walkerCount >= 1000000:
                endFlag = False
                print("Warning: Simulation terminates. Too many iterations.\n")
            else:
                pass

            if walkerCount % 10000 == 1 or endFlag == False:
                self.saveImages(walkerCount, clusterCount)

    def saveImages(self, walkerCount, clusterCount):
        if walkerCount == 1:
            if os.path.exists("Images"):
                pass
            else:
                os.mkdir("Images")

        print(walkerCount, "particles released.", clusterCount, "aggregated. Saving image ...")
        name = str(walkerCount) + ".png"
        cmap = colors.ListedColormap(['cadetblue', 'ghostwhite', 'powderblue'])
        plt.imshow(self.grid, interpolation = "hamming", cmap = cmap)
        plt.savefig("./Images/%s" % name)
        plt.close()
