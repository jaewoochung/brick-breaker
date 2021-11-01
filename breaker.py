import pygame
from pygame.locals import *
import wall_module
import paddle_module
import ball_module

pygame.init()

# define and set the screen
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Brick Breaker')

# define colors
bg = (240, 231, 219)
block_one = (192, 192, 192)
block_two = (105, 105, 105)
block_three = (47, 79, 79)

paddle_color = (75, 0, 130)
paddle_outline = (220, 218, 240)

# define game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0

player_paddle = paddle_module.Paddle()
ball = ball_module.Ball(paddle_module.paddle.x + (paddle_module.paddle.width // 2), paddle_module.paddle.y - paddle_module.paddle.height)

run = True
while run:

    clock.tick(fps)
    
    screen.fill(bg)
    
    # draw all objects
    # wall.draw_wall()
    wall_module.wall.draw_wall()
    paddle_module.paddle.draw()
    ball.draw()

    # game is live
    if live_ball:
        paddle_module.paddle.move()    
        game_over = ball.move()
        if game_over != 0:
            live_ball = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            ball.reset(paddle_module.paddle.x + (paddle_module.paddle.width // 2), paddle_module.paddle.y - paddle_module.paddle.height)
            paddle_module.paddle.reset()
            wall_module.wall.create_wall()
            
    pygame.display.update()
            
pygame.quit()
