import pygame

class Arrow:
    G = 0.2

    def __init__(self, screen, gameMap, x, y, ux, uy):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.gameMap = gameMap
        self.width = 6
        self.height = 3
        self.ux = ux
        self.uy = uy
        self.xi = self.x = x
        self.yi = self.y = y
        if ux > 0:
            self.xi = self.xi - self.width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.t = 0
        self.discard = 0

    def isDiscarded(self):
        return self.discard

    def isOut(self, x):
        return x < 0 or x > self.screenWidth

    def isGround(self, x):
        y = self.gameMap.getY(int(x))
        return self.y > y

    def move(self):
        if self.isOut(self.x) or self.isGround(self.x):
            self.discard = 1
        else:
            dx = (self.ux * self.t)
            dy = ((self.uy * self.t) - 0.5 * self.G * (self.t ** 2))
            x = self.xi - dx
            y = self.yi - dy
            self.t = self.t + 1
            self.rect = self.rect.move(x-self.x, y-self.y)
            self.x = x
            self.y = y

    def draw(self):
        pygame.draw.rect(self.screen, (255, 180, 0), self.rect)
