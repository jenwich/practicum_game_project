import pygame, math
from arrow import Arrow

pygame.mixer.init()
player_img = pygame.image.load("Archer.png")
arrows = []
counter = { "score": 0, "allBear": 0, "latestBear": 0, "comboBear": 0 }
bear_sound = pygame.mixer.Sound("sound/bear.wav")

class Player:
    def __init__(self, screen, gameMap):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.gameMap = gameMap
        self.moveDir = 0
        self.currentDir = 1
        self.speed = 2
        self.dead = 0

    def set(self, x, width, height):
        self.x = x
        self.y = self.gameMap.getY(self.x)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height, width, height)

    def getXY(self):
        return (self.x, self.y)

    def getSize(self):
        return (self.width, self.height)

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

    def isDead(self):
        return self.dead

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
        # pygame.draw.rect(self.screen, (225, 0, 0), self.rect)
        img_scaled = pygame.transform.scale(player_img, (self.width, self.height))
        if self.currentDir == 1:
            img_scaled = pygame.transform.flip(img_scaled, 1, 0)
        self.screen.blit(img_scaled, self.rect)

    def calculateU(self, t):
        if t < 300:
            return 3
        elif t < 1500:
            return t / 100
        else:
            return 15

    def setupArrow(self, dt, angle):
        u = self.calculateU(dt)
        ux = u * math.cos(angle)
        uy = u * math.sin(angle)
        if self.currentDir == 1:
            startX = self.x - self.width / 2
        if self.currentDir == 2:
            startX = self.x + self.width / 2
            ux = ux * -1
        arrow = Arrow(self.screen, self.gameMap, startX, self.y - self.height*0.75, ux, uy)
        arrows.append(arrow)

    def arrowsExec(self):
        for arrow in arrows:
            arrow.move()
            arrow.draw()
            if arrow.isDiscarded():
                arrows.remove(arrow)

    def hitBear(self, bears):
        for bear in bears:
            if bear.isHitPlayer(self):
                self.dead = 1

    def arrowHitBear(self, bears):
        for bear in bears:
            for arrow in arrows:
                if arrow.isHitBear(bear):
                    arrow.discard = 1
                    bear.hitted()
        for bear in bears:
            if bear.isDiscarded():
                global counter
                counter["allBear"] += 1
                counter["latestBear"] += 1
                counter["comboBear"] += 1
                bearPos = bear.getXY()
                dist = math.sqrt((self.x-bearPos[0])**2 + (self.y-bearPos[1])**2)
                sc = int(10 + dist * 0.1)
                counter["score"] += sc
                bear_sound.play()
                bears.remove(bear)
        for arrow in arrows:
            if arrow.isDiscarded():
                arrows.remove(arrow)

def clearArrows():
    del arrows[:]

def resetCounter():
    counter["score"] = 0
    counter["allBear"] = 0
    counter["latestBear"] = 0
    counter["comboBear"] = 0
