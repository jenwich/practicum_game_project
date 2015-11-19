import pygame

class Player:
    def __init__(self, screen, map):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.map = map

    def set(self, x, width, height):
        self.x = x
        self.y = self.map.get_y(self.x)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x-self.width/2, self.y-self.height, width, height)
        
    def can_move(self, x):
        return x-self.width/2 > 0 and x+self.width/2 < self.screen_width

    def move(self, x):
        if self.can_move(x):
            y = self.map.get_y(x)
            self.rect = self.rect.move(x-self.x, y-self.y)
            self.x = x
            self.y = y

    def draw(self):
        pygame.draw.rect(self.screen, (225, 0, 0), self.rect)
