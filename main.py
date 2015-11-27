import pygame, math
from gamemap import Map
from player import Player
from bear import *
from practicum import findDevices
from peri import PeriBoard

EVENT_MODE = 1 # 0 = mouse/keyboard, 1 = board
minLight = [9999, 9999, 9999]
maxLight = [0, 0, 0]
if EVENT_MODE == 1:
    devs = findDevices()
    if len(devs) == 0:
        print "*** No MCU board found."
        exit(1)
    board = PeriBoard(devs[0])
    print "*** MCU board found"
    print "*** Device manufacturer: %s" % board.getVendorName()
    print "*** Device name: %s" % board.getDeviceName()

    running = 1
    print "Adjust min-max light value, press the switch when done."
    while(running):
        for i in range(0, 3):
            light = board.getLight(i)
            running = not board.getSwitch()
            if light > maxLight[i]:
                maxLight[i] = light
            if light < minLight[i]:
                minLight[i] = light
    print (minLight[0], maxLight[0]), (minLight[1], maxLight[1]), (minLight[2], maxLight[2])

################################################

TITLE = "Let's hunt the little bears!"
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPMS = 100
BGCOLOR = (0, 125, 255)
PLAYER_WIDTH = 75
PLAYER_HEIGHT = 100
PLAYER_START_POS = SCREEN_WIDTH / 2
RELOAD_TIME = 250
BEAR_SPAWN_TIME = 2000

mode = 2 # 0 = exit, 1 = welcome, 2 = play
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

####################  PLAY  ######################
def play():
    gameMap = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    player = Player(screen, gameMap)
    player.set(PLAYER_START_POS, PLAYER_WIDTH, PLAYER_HEIGHT)
    running = 1
    mouseState = 0
    mouseTicks = 0
    bearTicks = 0
    angle = 0
    angleTicks = 0
    angleTextLabel = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global mode
                running = 0
                mode = 0

            ## Event Mouse & keyboard
            if EVENT_MODE == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.setDir(1)
                    if event.key == pygame.K_RIGHT:
                        player.setDir(2)
                elif event.type == pygame.KEYUP:
                    player.setDir(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if pygame.time.get_ticks() - mouseTicks >= RELOAD_TIME:
                        mouseState = 1
                        mouseTicks = pygame.time.get_ticks()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if mouseState == 1:
                        dt = pygame.time.get_ticks() - mouseTicks
                        player.setupArrow(dt, player.getAngle(event.pos[0], event.pos[1]))
                        mouseTicks = pygame.time.get_ticks()
                        mouseState = 0
                        print
        # Event board
        if EVENT_MODE == 1:
            led_left1 = board.getLight(0)
            led_left2 = board.getLight(1)
            led_right = board.getLight(2)
            angleText = pygame.font.Font(None, 36)
            if led_right > maxLight[2]:
                led_right = maxLight[2]
            elif led_right < minLight[2]:
                led_right = minLight[2]
            angle = (math.pi/2)-(math.pi * (led_right - minLight[2]))/(2 * (maxLight[2] - minLight[2]))
            switch = board.getSwitch()
            if led_left1 < 0.5*(maxLight[0]-minLight[0])+minLight[0]:
                player.setDir(1)
            elif led_left2 < 0.5*(maxLight[0]-minLight[0])+minLight[0]:
                player.setDir(2)
            else:
                player.setDir(0)
            if switch == True:
                if mouseState == 0:
                    mouseState = 1
                    mouseTicks = pygame.time.get_ticks()
                    board.setLedValue(0)
            elif switch == False:
                dt = pygame.time.get_ticks() - mouseTicks
                if mouseState == 1:
                    print angle*180/math.pi
                    player.setupArrow(dt, angle)
                    mouseTicks = pygame.time.get_ticks()
                    mouseState = 0

        if pygame.time.get_ticks() - bearTicks >= BEAR_SPAWN_TIME:
            spawnBear(screen, gameMap)
            bearTicks = pygame.time.get_ticks()
        screen.fill(BGCOLOR)
        if angleTextLabel == None:
            angleTextLabel = angleText.render(str(angle*180/math.pi), 1, (0, 0, 0))
        if pygame.time.get_ticks() - angleTicks > 100:
            angleTextLabel = angleText.render(str(angle*180/math.pi), 1, (0, 0, 0))
            angleTicks = pygame.time.get_ticks()
        screen.blit(angleTextLabel, (10, 10))
        gameMap.draw(screen)
        player.move()
        player.draw()
        player.arrowsExec()
        player.hitBear(bears)
        player.arrowHitBear(bears)
        bearsExec()
        pygame.display.flip()
        clock.tick(FPMS)

while mode != 0:
    if mode == 2:
        play()
