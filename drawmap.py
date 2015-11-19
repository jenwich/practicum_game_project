from map import Map
from player import Player
import pygame

pygame.init()

pygame.display.set_caption("Let's hunt the little bears!")
width = 1024
height = 600
screen = pygame.display.set_mode((width, height))

m = Map(width, height)
xylist = m.get_xylist()
running = 1
player = Player(screen, m)
player.set(width/2, 20, 50)
w = width/2
clock = pygame.time.Clock()
movedi = 0

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            movedi = 1
        if event.key == pygame.K_RIGHT:
            movedi = 2
    elif event.type == pygame.KEYUP:
        movedi = 0
    if movedi == 1:
        w = w-1
    elif movedi == 2:
        w = w+1

    screen.fill((0, 125, 255))
    m.draw(screen)
    player.move(w)
    player.draw()
    pygame.display.flip()

    clock.tick(150)
