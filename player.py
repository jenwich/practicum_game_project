import pygame, math
from arrow import Arrow

class Player:
    def __init__(self, screen, gameMap):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.gameMap = gameMap
        self.moveDir = 0
        self.currentDir = 1
        self.speed = 2
        self.arrows = []

    def set(self, x, width, height):
        self.x = x
        self.y = self.gameMap.getY(self.x)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height, width, height)

    def getAngle(self, x, y):
        mx = self.x
        my = self.y - self.height/2
        if x == mx:
            return math.pi / 2
        elif my - y < 0:
            return 0
        else:
            return math.atan(math.fabs(float(y - my)/(x - mx)))

    def isOut(self, x):
        return x - self.width/2 <= 0 or x + self.width/2 >= self.screenWidth

    def move(self):
        x = self.x
        if self.moveDir == 1:
            x = x - self.speed
        elif self.moveDir == 2:
            x = x + self.speed
        if self.moveDir != 0:
            if not self.isOut(x):
                y = self.gameMap.getY(x)
                self.rect = self.rect.move(x-self.x, y-self.y)
                self.x = x
                self.y = y

    def setDir(self, moveDir):
        self.moveDir = moveDir
        if moveDir != 0:
            self.currentDir = moveDir

    def draw(self):
        pygame.draw.rect(self.screen, (225, 0, 0), self.rect)

    def setupArrow(self, pos, angle):
        u = 10
        ux = u * math.cos(angle)
        uy = u * math.sin(angle)
        if self.currentDir == 2:
            ux = ux * -1
        arrow = Arrow(self.screen, self.gameMap, self.x, self.y - self.height/2, ux, uy)
        self.arrows.append(arrow)

    def arrowsExec(self):
        for arrow in self.arrows:
            arrow.move()
        for arrow in self.arrows:
            if arrow.isDiscarded():
                self.arrows.remove(arrow)
        for arrow in self.arrows:
            arrow.draw()
