import pygame

arrow_img = pygame.image.load("src/images/Arrow.png")

class Arrow:
    G = 0.2

    def __init__(self, screen, gameMap, x, y, ux, uy):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.gameMap = gameMap
        self.width = 30
        self.height = 15
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
        # pygame.draw.rect(self.screen, (255, 180, 0), self.rect)
        img_scaled = pygame.transform.scale(arrow_img, (self.width, self.height))
        if self.ux > 0:
            img_scaled = pygame.transform.flip(img_scaled, 1, 0)
        self.screen.blit(img_scaled, self.rect)

    def isHitBear(self, bear):
        x, y = int(self.x), self.y
        w, h = self.width, self.height
        px, py = bear.getXY()
        pw, ph = bear.getSize()
        if self.ux > 0:
            return x-w/2 >= px-pw/2 and x-2/w <= px+pw/2 and y >= py-ph and y <= py
        else:
            return x+w/2 >= px-pw/2 and x+w/2 <= px+pw/2 and y >= py-ph and y <= py
