import pygame
import random

class Map:
    X_STEP = 40
    Y_STEP = 5
    MIDDLE_RATE = 0.65
    HIGH_RATE = 0.9
    LOW_RATE = 0.4
    LINE_COLOR = (0, 125, 0)
    POLYGON_COLOR = (0, 200, 0)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.createXYList()
        self.memorizeY()

    def createXYList(self):
        self.xyList = []
        middle = self.height * self.MIDDLE_RATE
        high = self.height * self.HIGH_RATE
        low = self.height * self.LOW_RATE
        prev = middle
        for i in range(0, self.width + self.X_STEP, self.X_STEP):
            y = -1
            while y < low or y > high:
                r = random.randint(-10, 10) * self.Y_STEP
                y = prev + r
                prev = y
            self.xyList.append((i, int(y)))

    def memorizeY(self):
        self.yList = []
        for i in range(0, self.width):
            self.yList.append(self.calculateY(i))

    def calculateY(self, x):
        x1 = int(x / self.X_STEP)
        xy1 = self.xyList[x1]
        xy2 = self.xyList[x1+1]
        m = float(xy2[1] - xy1[1]) / (xy2[0] - xy1[0])
        y = m * (x - xy1[0]) + xy1[1]
        return int(y)

    def getXYList(self):
        return self.xyList

    def getY(self, x):
        return self.yList[x]

    def draw(self, screen):
        xyList = self.xyList
        prev_xy = xyList[0]
        for xy in xyList:
            pygame.draw.line(screen, self.LINE_COLOR, prev_xy, xy, 5)
            pygame.draw.polygon(screen, self.POLYGON_COLOR, [prev_xy, xy, (xy[0] ,self.height), (prev_xy[0], self.height)])
            prev_xy = xy
