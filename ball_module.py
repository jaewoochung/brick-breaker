import pygame
from pygame.locals import *
import wall_module
import paddle_module

pygame.mixer.init()

brick_sounds = pygame.mixer.Sound('sounds/sounds_brick.wav')
paddle_sounds = pygame.mixer.Sound('sounds/sounds_paddle.wav')
wall_sounds = pygame.mixer.Sound('sounds/sounds_wall.wav')
game_over_sound = pygame.mixer.Sound('sounds/arcade_sound_lost.mp3')

screen_width = 600
screen_height = 600

paddle_color = (75, 0, 130)
paddle_outline = (220, 218, 240)

screen = pygame.display.set_mode((screen_width, screen_height))

wall_module.init_wall()
paddle_module.init_paddle()

class Ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def draw(self):
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def move(self):

        collision_threshold = 5

        # start off with the assumption that the walls been destroyed completely
        wall_destroyed = 1
        row_count = 0
        for row in wall_module.wall.blocks:
            item_count = 0
            for item in row:
                # check collision for each one
                if self.rect.colliderect(item[0]):
                    brick_sounds.play()
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
                    if wall_module.wall.blocks[row_count][item_count][1] > 1:
                        wall_module.wall.blocks[row_count][item_count][1] -= 1
                    else:
                        # rectangle will exist but there will be no width/height
                        wall_module.wall.blocks[row_count][item_count][0] = (0,0,0,0)
                # check if block still exists, in which case the wall is not destroyed
                if wall_module.wall.blocks[row_count][item_count][0] != (0,0,0,0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        # after iterating through all the blocks, check to see if wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1
                        
        # check for collision with wall
        if self.rect.left < 0 or self.rect.right > screen_width:
            wall_sounds.play()
            self.speed_x *= -1

        # check for collision with top and bot of screen
        if self.rect.top < 0:
            wall_sounds.play()
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            game_over_sound.play()
            self.game_over = -1

        # collision with paddle
        if self.rect.colliderect(paddle_module.paddle):
            paddle_sounds.play()
            # collision from the top
            if abs(self.rect.bottom - paddle_module.paddle.rect.top) < collision_threshold and self.speed_y > 0:
                # ball is coming left to right towards the paddle
                if self.speed_x > 0:
                    # collision with left half of paddle mirror the direction on impact
                    if self.rect.midbottom >= paddle_module.paddle.rect.topleft and self.rect.midbottom <= paddle_module.paddle.rect.midtop:
                        self.speed_x *= -1
                # ball is coming right to left towards the paddle
                if self.speed_x < 0:
                    if self.rect.midbottom <= paddle_module.paddle.rect.topright and \
                       self.rect.midbottom >= paddle_module.paddle.rect.midtop:
                        self.speed_x *= -1
                
                self.speed_y *= -1
                self.speed_x += paddle_module.paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0
