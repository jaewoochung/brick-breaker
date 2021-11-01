import pygame
from pygame.locals import *

# colors 
block_one = (192, 192, 192)
block_two = (105, 105, 105)
block_three = (47, 79, 79)
bg = (240, 231, 219)

# display of the screen
screen = pygame.display.set_mode((600, 600))

rows = 6
cols = 6

# brick wall class
class Wall():
    def __init__(self):
        self.width = 600 // cols
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

def init_wall():
    global wall
    wall = Wall()
    wall.create_wall()
