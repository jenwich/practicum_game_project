import pygame
from gamemap import Map
from player import Player

TITLE = "Let's hunt the little bears!"
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPS = 100
BGCOLOR = (0, 125, 255)
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 50
PLAYER_START_POS = SCREEN_WIDTH / 2

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
gameMap = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
player = Player(screen, gameMap)
player.set(PLAYER_START_POS, PLAYER_WIDTH, PLAYER_HEIGHT)
clock = pygame.time.Clock()
running = 1

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player.setDir(1)
        if event.key == pygame.K_RIGHT:
            player.setDir(2)
    elif event.type == pygame.KEYUP:
        player.setDir(0)

    screen.fill(BGCOLOR)
    gameMap.draw(screen)
    player.move()
    player.draw()
    pygame.display.flip()

    clock.tick(FPS)
