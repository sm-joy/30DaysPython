from Settings import *
import pygame
class Segment:
    def __init__(self, _x: int, _y: int, _dir : int, _color: tuple[int, int, int]=(255, 255, 255)):
        self.dir = _dir
        self.rect = pygame.Rect(_x, _y, SNAKE_SIZE, SNAKE_SIZE)
        self.color = _color
    def set_pos(self, _x, _y):
        self.rect.x = _x
        self.rect.y = _y
 

class Snake:
    def __init__(self):
        self.head = Segment(_x=WINDOW_SIZE[0] // 2, _y=WINDOW_SIZE[1] // 2, _dir="LEFT")
        self.seggs = [self.head]
        self.velocityX, self.velocityY = 1,0

    def move(self, _dir: str, _dt: int=1)-> None:
        if _dir == "UP" and self.velocityY != 1:
            self.velocityX, self.velocityY = 0, -1
        elif _dir == "DOWN" and self.velocityY != -1:
            self.velocityX, self.velocityY = 0, 1
        elif _dir == "LEFT" and self.velocityX != 1:
            self.velocityX, self.velocityY = -1, 0
        elif _dir == "RIGHT" and self.velocityX != -1:
            self.velocityX, self.velocityY = 1, 0

        for i in range(len(self.seggs) - 1, 0, -1):
            self.seggs[i].dir = self.seggs[i - 1].dir
        self.head.dir = _dir 

        x = self.seggs[0].rect.x + self.velocityX * SNAKE_SPEED
        y = self.seggs[0].rect.y + self.velocityY * SNAKE_SPEED
        if 0 <= x and x < WINDOW_WIDTH - SNAKE_SIZE and 0 <= y and y < WINDOW_HEIGHT - SNAKE_SIZE:
            for i in range(len(self.seggs)-1, 0, -1):
                if i > 0:
                    self.seggs[i].set_pos(self.seggs[i-1].rect.x, self.seggs[i-1].rect.y)
            self.seggs[0].set_pos(x,y)

    def add_seg(self):
        self.seggs.append(Segment(self.seggs[-1].rect.x, self.seggs[-1].rect.y, _color=(80, 80,80), _dir=self.seggs[-1].dir))

    def draw(self, _surface)-> None:
        for seg in self.seggs:
            pygame.draw.rect(_surface, seg.color, seg.rect)
