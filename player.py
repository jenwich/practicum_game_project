import pygame

class Player:
    def __init__(self, screen, gameMap):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.gameMap = gameMap
        self.moveDir = 0
        self.speed = 2

    def set(self, x, width, height):
        self.x = x
        self.y = self.gameMap.getY(self.x)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height, width, height)

    def canMove(self, x):
        return x - self.width/2 > 0 and x + self.width/2 < self.screenWidth

    def move(self):
        x = self.x
        if self.moveDir == 1:
            x = x - self.speed
        elif self.moveDir == 2:
            x = x + self.speed
        if self.moveDir != 0:
            if self.canMove(x):
                y = self.gameMap.getY(x)
                self.rect = self.rect.move(x-self.x, y-self.y)
                self.x = x
                self.y = y

    def setDir(self, moveDir):
        self.moveDir = moveDir

    def draw(self):
        pygame.draw.rect(self.screen, (225, 0, 0), self.rect)
