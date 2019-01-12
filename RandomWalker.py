"""
This is the class for a random walker.
"""
import random

class Walker:
    def __init__(self, xstart, ystart):
        self.X = xstart
        self.Y = ystart

    # Walker is equally likely to move to up, down, left and right.
    def walk(self, N=1):
        for i in range(0, N):
            direction = random.randint(0, 3)
            if direction == 0:
                self.X += 1
            elif direction == 1:
                self.X += -1
            elif direction == 2:
                self.Y += 1
            else:
                self.Y += -1

    # Four commends will determine its next move, depending on its neighbors and region.
    # 2: Out of the field. -> Release a new particle.
    # Near 2 & 1: Aggregated to the cluster. The cluster reaches the boundary. -> Growth ends.
    # Near 1: Aggregated to the cluster. -> Release a new particle.
    # Near 0: Continue to walk.
    def checkAround(self, place, neighbors):
        if place == 2:
            return "out"
        elif 2 in neighbors and 1 in neighbors:
            return "end"
        elif 1 in neighbors:
            return "aggregated"
        else:
            return "continue"
