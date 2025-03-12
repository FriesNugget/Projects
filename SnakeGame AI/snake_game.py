import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple 
pygame.init() 

#create a font to use for game using the Python system font
#font = pygame.font.SysFont('arial', 25)
font = pygame.font.Font('Arial.ttf', 25)

# reset game after over

# reward

# play(action) -> direction

# game_iteration

#is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

#colors
WHITE =(255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20 # Size of the snake and food (in pixel)
INITAL_SPEED = 10 # speed when starting out
MAX_SPEED= 40 # the maximum speed 
SPEED_INCREMENT =0.5 # How much speed increase with each food eaten


class SnakeGameAI:

    def __init__(self, w=600, h=400):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock() #set game speed
        self.reset()

    def reset(self):
        #init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0 
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
        #set the speed when first playing
        self.speed = INITAL_SPEED 
    
    

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) *BLOCK_SIZE #random interger between 0 and the width - BLOCK_SIZE  // Multiple of the BLOCK_SIZE (random)
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) *BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake: #Make sure the food doesn't end up in the snake
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1 
        # collect the user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

               
        # move
        self._move(action) #update the head
        self.snake.insert(0, self.head)
        
        #reward for AI to learn what to do 
        reward = 0 

        # check if game over if it's then -10 to show AI it's not good // 
        # also if snake doesn't eat any food for too long (the longer the snake the more time it have left to find food)
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score


        # place new food or move 
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            #Increase speed with each food eaten 
            self.speed = min(self.speed + SPEED_INCREMENT, MAX_SPEED)
        else:
            self.snake.pop() # remove last element of snake

    
        # update ui and clock 
        self._update_ui()
        self.clock.tick(self.speed)

        #return reward, game over and score
        return reward, game_over, self.score
    

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        # check if wall
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        # check if hit itself
        if pt in self.snake[1:]:
            return True
        
        return False
    
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x,self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

    def _move(self, action):
        # direction 

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        # index of the current direction
        indx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[indx] #no change 
        elif np.array_equal(action, [0, 1, 0]):
            next_indx = (indx + 1) % 4 
            new_dir = clock_wise[next_indx] #right turn r -> d -> l -> u
        else: # [0,0,1]
            next_indx = (indx - 1) % 4 
            new_dir = clock_wise[next_indx] #left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y= self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y)

