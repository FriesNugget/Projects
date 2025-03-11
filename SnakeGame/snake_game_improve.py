import pygame
import random
from enum import Enum
from collections import namedtuple 
pygame.init() 

#create a font to use for game using the Python system font
#font = pygame.font.SysFont('arial', 25)
font = pygame.font.Font('Arial.ttf', 25)

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

BLOCK_SIZE = 20
INITAL_SPEED = 10 # speed when starting out
MAX_SPEED= 40 # the maximum speed 
SPEED_INCREMENT =0.5 # How much speed increase with each food eaten


class SnakeGame:

    def __init__(self, w=600, h=400):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock() #set game speed

        #init game state
        self.direction = Direction.RIGHT
        #set the speed when first playing
        self.speed = INITAL_SPEED 

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0 
        self.food = None
        self._place_food()
    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) *BLOCK_SIZE #random interger between 0 and the width - BLOCK_SIZE  // Multiple of the BLOCK_SIZE (random)
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) *BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake: #Make sure the food doesn't end up in the snake
            self._place_food()

    def play_step(self): 
        # collect the user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

                #making the game hard by pressing the opposite direction making the snake dead
                '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                '''

                #making the game more forgiving by not game over when pressing the opposite direction the snake going
            if event.type == pygame.KEYDOWN:
                #store the current direction before processing the input
                current_direction = self.direction

                #Directional input
                if event.key == pygame.K_LEFT:
                #change direction if not moving right
                    if current_direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                #change direction if not moving left
                    if current_direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                #change direction if not moving down
                    if current_direction != Direction.DOWN:
                        self.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                #change direction if not moving up
                    if current_direction != Direction.UP:
                        self.direction = Direction.DOWN
                    
        # move

        self._move(self.direction) #update the head
        self.snake.insert(0, self.head)
        
        # check if game over 
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score


        # place new food or move 
        if self.head == self.food:
            self.score += 1
            self._place_food()
            #Increase speed with each food eaten 
            self.speed = min(self.speed + SPEED_INCREMENT, MAX_SPEED)
        else:
            self.snake.pop() # remove last element of snake

    
        # update ui and clock 
        self._update_ui()
        self.clock.tick(self.speed)


        #return game over and score
        return game_over, self.score
    

    def _is_collision(self):

        # check if wall
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        
        # check if hit itself
        if self.head in self.snake[1:]:
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

    def _move(self, direction):
        x = self.head.x
        y= self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y)

if __name__ == '__main__':
    game = SnakeGame()

    #game loop
    while True: 
        game_over, score = game.play_step()

        if game_over == True:
            break
    print('Final Score', score)

    
    pygame.quit()