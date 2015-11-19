import random
import pygame
import math

class Map:
    STEP = 40
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.create_xlist()
        self.create_ylist()
        self.create_xylist()
        self.create_all_y()

    def create_xlist(self):
        self.xlist = []
        for i in range(0, self.width+self.STEP, self.STEP):
            self.xlist.append(i)

    def create_ylist(self):
        self.ylist = []
        middle = self.height * 0.65
        high = self.height * 0.9
        low = self.height * 0.4
        prev = middle
        for i in range(0, self.width+self.STEP, self.STEP):
            y = -1
            while y < low or y > high:
                r = random.randint(-10, 10) * 5
                y = prev + r
                prev = y
            self.ylist.append(int(y))

    def create_xylist(self):
        self.xylist = []
        for i in range(0, len(self.xlist)):
            self.xylist.append((self.xlist[i], self.ylist[i]))
    
    def create_all_y(self):
        self.y = []
        for i in range(0, self.width):
            self.y.append(self.calc_y(i))

    def get_xylist(self):
        return self.xylist

    def get_y(self, x):
        return self.y[x]

    def calc_y(self, x):
        x1 = int(x / self.STEP)
        xy1 = self.xylist[x1]
        xy2 = self.xylist[x1+1]
        m = float(xy2[1]-xy1[1])/(xy2[0]-xy1[0])
        y = m * (x - xy1[0]) + xy1[1]
        return int(y)

    def draw(self, screen):
        xylist = self.xylist
        prev_xy = xylist[0]
        for xy in xylist:
            pygame.draw.line(screen, (0, 125, 0), prev_xy, xy, 5)
            pygame.draw.polygon(screen, (0, 200, 0), [prev_xy, xy, (xy[0] ,self.height), (prev_xy[0], self.height)])
            prev_xy = xy
        
width = 640
height = 480
m = Map(width, height)
