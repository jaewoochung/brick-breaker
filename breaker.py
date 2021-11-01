import pygame
from pygame.locals import *

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

# brick wall class
class Wall():
    def __init__(self):
        self.width = screen_height // cols
        self.height = 35

    def create_wall(self):
        self.blocks = []
        # define an empty list for an indiv. block
        block_individual = []
        for row in range(rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # generate x and y positions in each block and create a rectanlge from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)

                # assign block strength
                if row  < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                else:
                    strength = 1
                # create a list at this point to store the rect and color data
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign color based on block strength
                if block[1] == 3:
                    block_color = block_three
                elif block[1] == 2:
                    block_color = block_two
                else:
                    block_color = block_one
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 1)

class Paddle():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 20
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

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

class Ball():
    def __init__(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

    def draw(self):
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def move(self):

        collision_threshold = 5

        # start off with the assumption that the wall has been destroyed completely
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # check collision for each one
                if self.rect.colliderect(item[0]):
                    # check if collision is from above
                    if abs(self.rect.bottom - item[0].top) < collision_threshold and self.speed_y > 0:
                        self.speed_y *= -1
                    # check from below
                    if abs(self.rect.top - item[0].bottom) < collision_threshold and self.speed_y < 0:
                        self.speed_y *= -1
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_threshold and self.speed_x > 0:
                        self.speed_x *= -1
                    # check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_threshold and self.speed_x < 0:
                        self.speed_x *= -1
                    # reduce the strength of the block
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        # rectangle will exist but there will be no width/height
                        wall.blocks[row_count][item_count][0] = (0,0,0,0)
                # check if block still exists, in which case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0,0,0,0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        # after iterating through all the blocks, check to see if wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1
                        
        # check for collision with wall
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # check for collision with top and bot of screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        # collision with paddle
        if self.rect.colliderect(player_paddle):
            # collision from the top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_threshold and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over
        
wall = Wall()
wall.create_wall()

player_paddle = Paddle()
ball = Ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:

    clock.tick(fps)
    
    screen.fill(bg)

    wall.draw_wall()
    
    player_paddle.draw()
    player_paddle.move()

    ball.draw()
    ball.move()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
            
pygame.quit()
