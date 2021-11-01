import pygame
from pygame.locals import *

# define and set the screen
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# define colors
paddle_color = (75, 0, 130)
paddle_outline = (220, 218, 240)

# define game variables
cols = 6
rows = 6

class Paddle():
    def __init__(self):
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.width = screen_width // cols
        self.height = 20
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

def init_paddle():
    global paddle
    paddle = Paddle()
