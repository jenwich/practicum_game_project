import pygame, random

bears = []
bear_img = pygame.image.load("bear2.png")

class Bear:
    width = 90
    height = 90
    hp = 1

    def __init__(self, screen, gameMap, moveDir, speed):
        self.screen = screen
        self.gameMap = gameMap
        self.moveDir = moveDir
        self.speed = speed * 0.3 + 0.5
        if moveDir == 1:
            self.x = self.width/2
        elif moveDir == 2:
            self.speed *= -1
            self.x = screen.get_width() - self.width/2
        self.y = self.gameMap.getY(self.x)
        self.xi = self.x
        self.yi = self.y
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height, self.width, self.height)
        self.discard = 0

    def getXY(self):
        return (self.x, self.y)

    def getSize(self):
        return (self.width, self.height)

    def isOut(self, x):
        if self.moveDir == 1:
            return x + self.width/2 >= self.screen.get_width()
        elif self.moveDir == 2:
            return x - self.width/2 <= 0

    def move(self):
        x = self.x + self.speed
        if not self.isOut(x):
            y = self.gameMap.getY(int(x))
            self.rect = self.rect.move(int(x - self.xi) - int(self.x - self.xi), y - self.y)
            self.x = x
            self.y = y
        else:
            self.discard = 1

    def isDiscarded(self):
        return self.discard

    def draw(self):
        # pygame.draw.rect(self.screen, (0, 0, 255), self.rect)
        img_scaled = pygame.transform.scale(bear_img, (self.width, self.height))
        if self.moveDir == 1:
            img_scaled = pygame.transform.flip(img_scaled, 1, 0)
        self.screen.blit(img_scaled, self.rect)

    def isHitPlayer(self, player):
        x, y = int(self.x), self.y
        w, h = self.width, self.height
        px, py = player.getXY()
        pw, ph = player.getSize()
        return ((x-w/2 >= px-pw/2) and (x-w/2 <= px+pw/2)) or ((x+w/2 >= px-pw/2) and (x+w/2 <= px+pw/2))

    def hitted(self):
        self.hp = self.hp - 1
        if self.hp == 0:
            self.discard = 1

def spawnBear(screen, gameMap):
    r1 = random.randint(1, 2)
    r2 = random.randint(1, 3)
    bear = Bear(screen, gameMap, r1, r2)
    bears.append(bear)

def bearsExec():
    for bear in bears:
        bear.move()
        bear.draw()
        if bear.isDiscarded():
            bears.remove(bear)
