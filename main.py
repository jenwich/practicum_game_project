import pygame, math, time
from gamemap import Map
from player import *
from bear import *
from practicum import findDevices
from peri import PeriBoard

######################  CONSTANTS  ########################

EVENT_MODE = 1 # 0 = mouse/keyboard, 1 = board
TITLE = "Let's hunt the little bears!"
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPMS = 100
BGCOLOR = (135, 206, 250)
PLAYER_WIDTH = 75
PLAYER_HEIGHT = 100
PLAYER_START_POS = SCREEN_WIDTH / 2
RELOAD_TIME = 300

#####################  BOARD SETUP  #######################

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

###########################################################

displayMode = 1 # 0 = exit, 1 = welcome, 2 = play, 3 = game over
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.mixer.music.load("src/sounds/BackgroundSong.wav")
pygame.mixer.music.set_volume(0.4)
shoot_sound = pygame.mixer.Sound("src/sounds/Shoot.wav")
ultimate_sound = pygame.mixer.Sound("src/sounds/Wind.wav")
gameOverSwitchCount = 0
gameOverSwitchState = 0

####################  NEW GAME SETUP  #####################

gameMap = None
player = None
bearSpawnTime = 2000
def newGame():
    global gameMap, player, bearSpawnTime
    gameMap = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    player = Player(screen, gameMap)
    player.set(PLAYER_START_POS, PLAYER_WIDTH, PLAYER_HEIGHT)
    bearSpawnTime = 2000
    clearArrows()
    clearBears()
    resetCounter()
    pygame.mixer.music.play(-1)

#########################  PLAY  ##########################

def play():
    # Initialize playing
    global gameMap, player, bearSpawnTime
    newGame()
    mouseState = 0
    mouseTicks = 0
    bearTicks = 0
    angle = 0
    angleTicks = 0

    # Define text
    angleText = pygame.font.Font(None, 28)
    angleTextLabel = angleText.render(str(0), 1, (0, 0, 0))
    scoreText = pygame.font.Font(None, 28)
    scoreTextLabel = scoreText.render(str(0), 1, (0, 0, 0))
    bearText = pygame.font.Font(None, 28)
    bearTextLabel = bearText.render(str(0), 1, (0, 0, 0))

    while displayMode != 0:
        for event in pygame.event.get():
            # When close window
            if event.type == pygame.QUIT:
                global displayMode
                displayMode = 0
                if EVENT_MODE == 1:
                    board.setLedValue(0)

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

        # Draw map and background
        screen.fill(BGCOLOR)
        gameMap.draw(screen)

        ## Play Screen
        if displayMode == 2:

            # Speed up bears spawn time
            if counter["latestBear"] >= 5:
                counter["latestBear"] = 0
                bearSpawnTime = int(bearSpawnTime * 0.9)

            # Check if can bear spawn now
            if pygame.time.get_ticks() - bearTicks >= bearSpawnTime:
                spawnBear(screen, gameMap)
                bearTicks = pygame.time.get_ticks()

            # Event: board
            if EVENT_MODE == 1:

                # Define censor variables
                switch = board.getSwitch()
                ldr_left1 = board.getLight(0)
                ldr_left2 = board.getLight(1)
                ldr_right = board.getLight(2)
                sound = board.getSound()

                # Adjust the right LDR to be in range
                if ldr_right > maxLight[2]:
                    ldr_right = maxLight[2]
                elif ldr_right < minLight[2]:
                    ldr_right = minLight[2]

                # Calculate Angle
                angle = 0.1*(math.pi * (ldr_right - minLight[2]))/(2 * (maxLight[2] - minLight[2])) + 0.9*angle

                # Set player move direction
                if ldr_left1 < 0.5*(maxLight[0]-minLight[0])+minLight[0]:
                    player.setDir(1)
                elif ldr_left2 < 0.5*(maxLight[1]-minLight[1])+minLight[1]:
                    player.setDir(2)
                else:
                    player.setDir(0)

                # Check if can player shoot arrow now
                if switch == True:
                    if mouseState == 0:
                        mouseState = 1
                        mouseTicks = pygame.time.get_ticks()
                elif switch == False:
                    dt = pygame.time.get_ticks() - mouseTicks
                    if mouseState == 1:
                        if dt > RELOAD_TIME:
                            player.setupArrow(dt, angle)
                            shoot_sound.play()
                        mouseTicks = pygame.time.get_ticks()
                        mouseState = 0

                # Check if can use ultimate shot now
                if counter["comboBear"] >= 10:
                    board.setLed(2, 1)
                    if sound < 200:
                        counter["comboBear"] = 0
                        ultimate_sound.play()
                        clearBears()
                else:
                    board.setLed(2, 0)

            # Update texts
            if pygame.time.get_ticks() - angleTicks > 100:
                angleTextLabel = angleText.render("Angle: "+str(int(angle*180/math.pi)) , 1, (0, 0, 0))
                scoreTextLabel = scoreText.render("Score: "+str(counter["score"]) , 1, (0, 0, 0))
                bearTextLabel = bearText.render("Bears: "+str(counter["allBear"]) , 1, (0, 0, 0))
                angleTicks = pygame.time.get_ticks()

            # Blit texts to screen
            playerPos = player.getXY()
            screen.blit(angleTextLabel, (playerPos[0]-PLAYER_WIDTH/2, playerPos[1]+10))
            screen.blit(scoreTextLabel, (SCREEN_WIDTH - 150, 10))
            screen.blit(bearTextLabel, (SCREEN_WIDTH - 150, 40))

            # Check if player is dead
            if player.isDead():
                displayMode = 3

            # Execute events
            player.move()
            player.draw()
            player.arrowsExec()
            player.hitBear(bears)
            player.arrowHitBear(bears)
            bearsExec()

        ## Welcome Screen
        elif displayMode == 1:
            welcomeText = pygame.font.Font(None, 48)
            guideText = pygame.font.Font(None, 28)
            welcomeTextLabel = welcomeText.render("Let's hunt the little bears", 1, (0, 0, 0))
            guideTextLabel = guideText.render("Press the switch to play the game", 1, (0, 0, 0))
            screen.blit(welcomeTextLabel, (SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2 - 150))
            screen.blit(guideTextLabel, (SCREEN_WIDTH/2 - 160, SCREEN_HEIGHT/2 - 100))
            if EVENT_MODE == 1:
                sw = board.getSwitch()
                if sw == 1:
                    mouseTicks = pygame.time.get_ticks()
                    displayMode = 2

        ## Game over Screen
        elif displayMode == 3:
            pygame.mixer.music.stop()
            gameOverText = pygame.font.Font(None, 48)
            scoreText = pygame.font.Font(None, 36)
            gameOverTextLabel = gameOverText.render("Game Over", 1, (0, 0, 0))
            scoreTextLabel = scoreText.render("Score: "+ str(counter["score"]) +"   Bears: "+ str(counter["allBear"]), 1, (0, 0, 0))
            screen.blit(gameOverTextLabel, (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 150))
            screen.blit(scoreTextLabel, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 100))
            if EVENT_MODE == 1:
                global gameOverSwitchCount, gameOverSwitchState
                sw = board.getSwitch()
                if sw == 1:
                    gameOverSwitchState = 1
                elif sw == 0:
                    if gameOverSwitchState == 1:
                        gameOverSwitchCount += 1
                        gameOverSwitchState = 0
                if gameOverSwitchCount == 5:
                    gameOverSwitchCount = 0
                    newGame()
                    displayMode = 2

        pygame.display.update()
        clock.tick(FPMS)

play()
